# este script corre sobre windows
# scraping gallito

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


# website en alquiler de inmuebles
website = "https://www.gallito.com.uy"

driver = webdriver.Chrome()
driver.get(website)
driver.maximize_window()

# esperar que cargue pagina
time.sleep(4)

# elemento del menu
elemento = driver.find_element(By.XPATH, '//*[@id="cat_inmuebles_li"]/a')

# Mueve el mouse sobre el elemento para desplegar menu
action = ActionChains(driver)
action.move_to_element(elemento).perform()

time.sleep(2)

# click en el menu de alquileres
menu_alquileres = driver.find_element(By.XPATH, '//div[@id="cat_inmuebles"]/div[2]/ul/li[2]/h3/a')
menu_alquileres.click()

time.sleep(1)

# lista en la que se van a guardar los datos de cada publicacion
lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(2):

    if i > 0:
        # avanzo a la siguiente pagina
        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="paginador"]/ul/li[6]/a')
        avanzar_pag.click()
        time.sleep(2)

    else:
        time.sleep(4)
        # captura la lista de elementos de alquiler
        lst_alquiler = driver.find_elements(By.XPATH, '//div[3]/div[1]/div/div[1]/a')

        # creo una lista con las urls para que no pierda la informacion al hacer el back()
        urls_alquiler = []
        for alquiler in lst_alquiler:
            url_alquiler = alquiler.get_attribute('href')
            urls_alquiler.append(url_alquiler)

        # abre cada uno de los url de alquileres
        for url_alquiler in urls_alquiler:

            # abrir enlace
            driver.get(url_alquiler)
            time.sleep(2)

            # capturar informacion de url abierta
            try:
                id = "gallito_{}".format(url_alquiler.split("-")[-1])
                precioString = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/div[2]/span').text
                precio = float(precioString.split(" ")[-1].replace(".",""))
                moneda = precioString.split(" ")[0]
            except Exception:
                pass
            try:
                departamento = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[5]/a').text
                zona = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[6]/a').text
                tipo_propiedad = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[1]/p').text
            except Exception:
                pass
            try:
                banos = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[5]/p').text
                metros = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[6]/p').text
                dormitorios = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[4]/p').text
            except Exception:
                pass
            try:
                # voy a seccion de ubicacion
                place_map = driver.find_element(By.XPATH, '//*[@id="ulNavGaleria"]/li[4]/a')
                place_map.click()
                time.sleep(1)

                url_map = driver.find_element(By.XPATH, '//*[@id="iframeMapa"]')
                src = url_map.get_attribute('src')
                lat = src.split("=")[2].split(",")[0][:11]
                lon = src.split("=")[2].split(",")[-1][:11]


            except Exception :
                pass

            # guardar informacion en diccionario
            try:
                dic_alquiler = {
                    "id": id,
                    "url_link": url_alquiler,
                    "price": precio,
                    "exchange": str(moneda),
                    "state_name": departamento,
                    "city_name": zona,
                    "PROPERTY_TYPE": tipo_propiedad,
                    "TOTAL_AREA": metros,
                    "FULL_BATHROOMS": banos,
                    "BEDROOMS": dormitorios,
                    "location": {
                        "latitude": float(lat),
                        "longitude": float(lon)
                    },
                    "imagenes": []
                }
                lst_data.append(dic_alquiler)
            except Exception:
                pass

            # volver a la pagina anterior
            driver.back()
            time.sleep(2)


#---------------------------------------------------------------
#---------------------------------------------------------------


# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('gallito.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# input("Enter para salir..")

# cerrar driver
driver.quit()
