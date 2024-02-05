# Clase para la lectura de parámetros desde el fichero de configuracion ../configs/config_variables.yml

import yaml
import logging


class lecturaconfiguracion:
    """
    Clase que leer del fichero de configuracion situado en ../configs/config_variables.yml, todas las
    variables externas como rutas, nombres de sites, parametros para el crawler,etc.
    """

    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.INFO)

    def __init__(self, ruta_config: str):
        """
        :param ruta_config:
        Inicializa la clase como entrada recibe la ruta del fichero de configuracion yml
        """
        self.ruta_config = ruta_config

        with open(fr'{ruta_config}') as f:
            parametros_yml = yaml.load(f, Loader=yaml.FullLoader)

        self.parametros_yml = parametros_yml

    def get_folders_crawler(self) -> list:
        """
        :return:
        Devuelve un Array con la informacion de las carpetas de descarga para el crawler
        """

        folders = []
        for clave in self.parametros_yml['RUTA_SITE_DESCARGA']:
            folders.append(self.parametros_yml['RUTA_SITE_DESCARGA'][clave])

        logging.info(f'Ruta de la escritura de datos: {folders}')

        return folders

    def get_urls_crawler(self) -> list:
        """
        :return:
        Devuelve un array con la información de las urls a descargar con el crawler
        """

        urls = []
        for clave in self.parametros_yml["URLS_DESCARGA"]:
            urls.append(self.parametros_yml["URLS_DESCARGA"][clave])

        logging.info(f'URLS de Descarga: {urls}')

        return urls

    def get_lista_blanca_crawler(self) -> list:
        """
        :return:
        Devuelve el valor leido para la lista blanca del Crawler (elementos a descargar)
        """

        lista_blanca = []
        for clave in self.parametros_yml["LISTA_BLANCA"]:
            lista_blanca.append(self.parametros_yml["LISTA_BLANCA"][clave])

        logging.info(f'Elementos a Descargar: {lista_blanca}')

        return lista_blanca

    def get_ruta_base_descarga(self) -> str:
        """
        :return: Ruta Base para las descargas de crawler
        Devuelve la ruta base a partir de la cual se decargarn las páginas en crudo.
        """

        ruta_base_descarga = self.parametros_yml["RUTA_BASE_DESCARGAS_CRAWLER"]

        logging.info(f'Obtenemos la ruta base de descarga: {ruta_base_descarga}')

        return ruta_base_descarga

    def get_numero_paginas_descargadas(self) -> int:
        """
        :return: Numero de páginas a descargar por el Crawler
        Devuelve el número de páginas que decargar el Crawler después parara el proceso.
        """

        num_paginas_descarga = self.parametros_yml["NUMERO_PAG_DESCARGAS"]

        logging.info(f'Obtenemos el numero de páginas a descargar: {num_paginas_descarga}')

        return int(num_paginas_descarga)

    def get_enable_crawler(self) -> int:
        """
        :return: Numero que indica si se habilita el Crawler 0 - No habilitado, habilitado != 0
        Devuelve el número que indica si se habilita el paso del crawler.
        """

        enable_crawler = self.parametros_yml["ENABLE_CRAWLER"]

        logging.info(f'Obtenemos el numero que indica si se habilita en crawler: {enable_crawler}')

        return int(enable_crawler)

    def get_user_agent(self) -> str:
        """
        :return: User Agent (Navegador) usado para las peticiones requests
        Devuelve el user agent que queremos usar.
        """

        user_agent = self.parametros_yml["USER_AGENT"]

        logging.info(f'Obtenemos el user agent: {user_agent}')

        return user_agent