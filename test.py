from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.binary_location = r'C:\chromedriver\chrome.exe'
driver = webdriver.Firefox()

driver.get("https://www.bvc.com.co/mercado-local-en-linea?tab=renta-variable_mercado-global-colombiano")
driver.implicitly_wait(1)
driver.maximize_window()
# elem = driver.find_element(By.XPATH,'/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]')

# selector para desplegar el calendario
elem = driver.find_element(By.CSS_SELECTOR, ".OCIcon__Svg-sc-hhr8al-0")
elem.click()
driver.implicitly_wait(1)

# selector para pasar a vista de año
elem = driver.find_element(By.CSS_SELECTOR, ".DatePickerstyled__StyledNavigationLabel-sc-nz7bkq-2")
elem.click()

# selector para elegir un mes en particular, cambiar el número por el mes del que se desea descargar la información
elem = driver.find_element(By.CSS_SELECTOR, "button.react-calendar__tile:nth-child(1)")
driver.implicitly_wait(1)

# driver.get("https://www.bvc.com.co/mercado-local-en-linea?tab=renta-variable_mercado-global-colombiano")

# elem2 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]/abbr[1]')
# elem2.click()
# elem3 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[5]/div[2]/div[1]/button[1]')
# elem3.click()
driver.close()

