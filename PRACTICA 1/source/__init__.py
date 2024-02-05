import logging
from clases.crawler import crawler
from clases.obtenerInformacion import obtenerInformacion
from clases.lecturaconfiguracion import lecturaconfiguracion
import csv

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

LectorConfig_yml = lecturaconfiguracion('configs/config_variables.yml')

folders = LectorConfig_yml.get_folders_crawler()
urls = LectorConfig_yml.get_urls_crawler()
lista_blanca = LectorConfig_yml.get_lista_blanca_crawler()
ruta_base_descarga = LectorConfig_yml.get_ruta_base_descarga()
numero_paginas_descargadas = LectorConfig_yml.get_numero_paginas_descargadas()
enable_crawler = LectorConfig_yml.get_enable_crawler()
user_agent = LectorConfig_yml.get_user_agent()



# En la fase uno recorremos la página de wallapop y nos desccargamos su contenido

if(enable_crawler != 0):
    for (folder, url) in zip(folders, urls):
        logging.info(f'Extrayendo informacion de {url} y almacenandola en {folder}')
        Crawler_obj = crawler(urls=[url], folder=folder)
        Crawler_obj.set_lista_blanca(lista_blanca)
        Crawler_obj.set_ruta_raiz_descarga(ruta_base_descarga)
        Crawler_obj.set_numero_paginas_descargar(numero_paginas_descargadas)
        Crawler_obj.set_user_agent(user_agent)
        Crawler_obj.run()

# Procesamos de tranformacion de datos a Dataset

extractor_caracteristicas = obtenerInformacion(folder_wallapop=ruta_base_descarga)
for folder in folders:
    for item_lista in lista_blanca:
        extractor_caracteristicas.set_ruta_items(folder=folder + '/' + item_lista)
        if item_lista == 'item':
            df_items = extractor_caracteristicas.procesar_items()

df_items.to_csv('datos/csv_items.csv', quotechar='"', escapechar='\\', sep=';', quoting=csv.QUOTE_MINIMAL)

logging.info(df_items.head())
