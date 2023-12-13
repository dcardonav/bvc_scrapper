# BVC Scrapper

Esta herramienta permite la descarga automática de la información de Mercado en Línea de la BVC, tanto para mercardo local como global. Funciona mediante el uso de la librería selenium para para la información más reciente (5 años) y para la  más antigua emplea la función de lectura de tablas html incorporada en pandas.

El código tiene múltiples oportunidades de mejora, en particular una vectorización de los ciclos, la utilización de un archivo de configuración y la separación en funciones, e.g., una función para seleccionar una fecha, otra para descargar un archivo, etc.; sin embargo, mi principal interés era obtener la información histórica más que desarrollar una herramienta.


## Librerías Utilizadas
- **Python:** La herramienta se probó con las versiones 3.11 y 3.12
- **selenium:** Una de las librerías más utilizadas para web scrapping, especialmente por su facilidad para identificar elementos bien sea con consultas XPath, estructuras DOM o CSS (como es el caso de la presente herramienta). El código está configurado para utilizar Firefox, en caso de emplear Chrome u otro navegador se debe verificar la instalación del respectivo driver.
- **pandas**: La librería por excelencia cuando se está trabajando con un bajo volumen de datos tabulares (~300k registros). En este código se utiliza para leer los datos directamente del HTML en los años donde la página no permite la descarga y para unificar todos los archivos en un único dataset.


## Utilización

- Verficar que se cuenta con las librerías requeridas y el driver para el navegador, el código asume que se tiene Firefox.
- Establecer el valor de las variables ```anio``` y ```mes``` que corresponden al **mes final** del período a descargar.
- Ejecutar como un script en el ambiente de preferencia

## Funcionamiento Básico

### Navagación de la Página

El archivo ``` test.py ``` contiene el código básico que realiza la navegación y descarga de la información de un año en particular. Es básicamente un ciclo anidado que navega meses en orden descendente y los días de cada mes en ascendente.

``` python3
anio = 2023
mes = 12
mayor_cinco_anios = False
hoy = datetime.date.today()     # necesario para información antigua
for i in range(mes, 0, -1):
    j = 1¡
    max_day = -1
    while (j < max_day) or max_day == -1:
        # selector para desplegar el calendario
        elem = driver.find_element(By.CSS_SELECTOR, ".OCIcon__Svg-sc-hhr8al-0")
        elem.click()
        time.sleep(1)

```
La variable ```max_day``` se utiliza para la navegación de los días ya que el calendario react presenta 35 o 42 días dependiendo del mes.

El código cambia el calendario a la vista de año navegando hasta el actual, luego selecciona el mes actual usando el vector ```nthchild()``` del calendario. 

Otra parte del código tiene que ver con la obtención de la información más antigua que cinco años.

``` python3
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
```
En este caso, si la fecha es más antigua que cinco años, el código leerá los datos directamente del html de lo contrario dará click en el botón de descarga.


### Unificación de Datos

El archivo ```compile.py``` contiene código básico para la unificación de los archivos descargados; usa una expresión regular básica para buscar todos los archivos e itera sobre cada uno, les agrega una columna de fecha y los envía a un ```Dataframe```; una vez termina el ciclo unifica todos los dataframes y guarda el resultado en un archivo Excel.
