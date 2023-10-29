__author__ = "David Cardona-Vasquez"
__copyright__ = "Copyright 2023, David Cardona-Vasquez"
__credits__ = ["David Cardona-Vasquez"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "David Cardona-Vasquez"
__status__ = "Development"

import datetime
import io
import os.path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time


# dónde se almacenará la información descargada, por defecto asume la existencia de una
# carpeta llamada historicos donde se encuentra el proyecto
ruta_descarga = os.path.join(os.getcwd(), "historicos")
# tiempo en segundos a esperar después de seleccionar una fecha particular, entre más
# lenta sea la conexión, mayor debe ser el valor
espera_datos = 3


#configuración de los datos a consultar, el prefijo corresponde al nombre que tendrá
# el archivo descargado

# para mercado global
# mercado = "renta-variable_mercado-global-colombiano"
# prefijo = "RVMGC_"

# para mercado local
prefijo = "RVLocal_"
mercado = "renta-variable_mercado-global-colombiano"


# opciones de configuración del driver, en este caso para Firefox.
options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", ruta_descarga)
# esta opción habilita la descarga automática sin preguntar
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
driver = webdriver.Firefox(options=options)

driver.get("https://www.bvc.com.co/mercado-local-en-linea?tab="+mercado)
driver.implicitly_wait(1)
driver.maximize_window()

elem = driver.find_element(By.CSS_SELECTOR, "h3.kmcgzx")
elem.click()
elem = driver.find_element(By.CSS_SELECTOR, ".Tooltipstyled__CloseTooltip-sc-fwz25g-14")
elem.click()
driver.implicitly_wait(1)


# El código funciona desde el último mes hasta el primero, dado que el ejemplo está con 2023, el último mes
# disponible en este momento es octubre
anio = 2023
mes = 12
mayor_cinco_anios = False
hoy = datetime.date.today()     # necesario para información antigua
for i in range(mes, 0, -1):
    j = 1
    max_day = -1
    while (j < max_day) or max_day == -1:
        # selector para desplegar el calendario
        elem = driver.find_element(By.CSS_SELECTOR, ".OCIcon__Svg-sc-hhr8al-0")
        elem.click()
        time.sleep(1)

        # selector para pasar a vista de año
        elem = driver.find_element(By.CSS_SELECTOR, ".DatePickerstyled__StyledNavigationLabel-sc-nz7bkq-2")
        elem.click()


        cur_year = int(driver.find_element(By.CSS_SELECTOR, ".react-calendar__navigation__label__labelText").text)

        # mover a un año antes hasta que estemos en el que queremos descargar
        while cur_year != anio:
            elem = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__navigation__arrow:nth-child(2)")
            elem.click()
            time.sleep(1)
            cur_year = int(driver.find_element(By.CSS_SELECTOR, ".react-calendar__navigation__label__labelText").text)

        month = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(" + str(i) + ")")
        cur_month = month.accessible_name.split()[1]
        # truco para evitar problemas con la interfaz del chatbot
        driver.execute_script("window.scrollTo(0, 50)")
        month.click()
        time.sleep(1)

        # truco para lidiar con el tamaño variable del calendario
        try:
            aux_max_day = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(42)")
            max_day = 42
        except NoSuchElementException:
            max_day = 35

        day = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child("+str(j)+")")
        while True:
            if not(cur_month in day.accessible_name) and j < max_day:
                j = j+1
                day = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(" + str(j) + ")")
            else:
                break
        # truco para evitar problemas con la interfaz del chatbot
        driver.execute_script("window.scrollTo(0, 120)")
        day.click()
        # en caso de que la conexión sea lenta, damos tiempo para que se carguen los datos,
        # se puede hacer mirando el la respuesta, pero esta es la forma quick and dirty
        time.sleep(espera_datos)

        # traemos la fecha del calendario y luego la convertimos a fecha para
        # comparar si es antigua
        fecha_str = driver.find_element(By.CSS_SELECTOR, '.react-date-picker__inputGroup > input:nth-child(1)')
        aux_fecha = datetime.datetime.strptime(fecha_str.get_attribute("value"), '%Y-%m-%d').date()
        if (hoy - aux_fecha).days / 365 > 5:
            mayor_cinco_anios = True
        else:
            # bloque innecesario si el código se ejecuta en el flujo correcto
            mayor_cinco_anios = False
        if mayor_cinco_anios:
            # si es mayor a cinco años, es necesario sacar los datos del elemento table
            df = pd.read_html(io.StringIO(driver.page_source))
            if len(df) == 1 and df[0].shape[0] > 1:
                df = df[0]
                df.iloc[:, 2] = df.iloc[:, 2].str.replace('%', '')
                df.iloc[:, 2] = df.iloc[:, 2].str.replace('-', '0')
                df.iloc[:, 2] = df.iloc[:, 2].str.replace(',', '')
                df.iloc[:, 2] = df.iloc[:, 2].astype(float)
                df.to_csv(os.path.join(ruta_descarga,
                                       prefijo+str(aux_fecha.year) +
                                       str("{:02d}".format(aux_fecha.month)) +
                                       str("{:02d}".format(aux_fecha.day))+".csv"),
                          sep= ";", decimal=",", index=False)
            j = j + 1
        else:
            try:
                descarga = driver.find_element(By.CSS_SELECTOR, ".jlIRBY")
            except NoSuchElementException:
                continue
            finally:
                j = j + 1

            descarga.click()
            time.sleep(1)
            close_download = driver.find_element(By.CSS_SELECTOR, ".sc-EgOXT")
            close_download.click()
            time.sleep(1)


driver.close()

