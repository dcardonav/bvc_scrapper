from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import NoSuchElementException

import time

options = Options()
options.binary_location = r'C:\chromedriver\chrome.exe'
driver = webdriver.Firefox()

driver.get("https://www.bvc.com.co/mercado-local-en-linea?tab=renta-variable_mercado-global-colombiano")
driver.implicitly_wait(1)
driver.maximize_window()
# elem = driver.find_element(By.XPATH,'/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]')

# selector para elegir un mes en particular, cambiar el número por el mes del que se desea descargar la información
# elem = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(1)")
# driver.implicitly_wait(1)

elem = driver.find_element(By.CSS_SELECTOR, "h3.kmcgzx")
elem.click()
elem = driver.find_element(By.CSS_SELECTOR, ".Tooltipstyled__CloseTooltip-sc-fwz25g-14")
elem.click()
driver.implicitly_wait(1)
for i in range(3, 4):
    j = 1
    while j < 35:
        # selector para desplegar el calendario
        elem = driver.find_element(By.CSS_SELECTOR, ".OCIcon__Svg-sc-hhr8al-0")
        elem.click()
        time.sleep(1)

        # selector para pasar a vista de año
        elem = driver.find_element(By.CSS_SELECTOR, ".DatePickerstyled__StyledNavigationLabel-sc-nz7bkq-2")
        elem.click()

        month = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(" + str(i) + ")")
        month.click()

        day = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child("+str(j)+")")
        while True:
            if not("marzo" in day.accessible_name):
                j = j+1
                day = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(" + str(j) + ")")
            else:
                break
        day.click()
        time.sleep(1)
        try:
            descarga = driver.find_element(By.CSS_SELECTOR, ".jlIRBY")
        except NoSuchElementException:
            continue
        finally:
            j = j + 1
        descarga.click()

        close_download = driver.find_element(By.CSS_SELECTOR, ".sc-EgOXT")
        close_download.click()
        time.sleep(1)







# driver.get("https://www.bvc.com.co/mercado-local-en-linea?tab=renta-variable_mercado-global-colombiano")

# elem2 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]/abbr[1]')
# elem2.click()
# elem3 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[5]/div[2]/div[1]/button[1]')
# elem3.click()
driver.close()

