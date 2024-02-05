# Crawling
# Imports Seccion

from urllib.parse import urlparse
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import locale
import os
import requests.exceptions


class crawler:
    """
    Clase preparada para recorrer un portal y descargarse en una ruta prefijada todas sus páginas
    Es completamente configurable, User Agent, Profundidad, robots, excepcionar rutas
    """

    os.environ["PYTHONIOENCODING"] = "utf-8"
    myLocale = locale.setlocale(category=locale.LC_ALL, locale="es_ES.UTF-8")

    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.INFO)

    def __init__(self, urls=[], folder: str = 'raiz'):
        """
        :param urls:
        :param folder:
        Constructor de la clase, recube como parámetros las urls descarga en una array
        la ruta de descarga de los estáticos de la web
        """
        self.folder = folder
        self.visited_urls = []
        self.urls_to_visit = urls
        self.lista_blanca = []
        self.ruta_raiz_descarga = "datos"
        self.contador_paginas = 0
        self.limite_paginas_descargadas = -1 # Por defecto sin limite
        self.user_agent = "My User Agent" # Por defecto Usamos Chrome

        logging.info(f'Iniciando la Clase CRAWLER para extraer informacion de {urls}')

    def set_user_agent(self, user_agent):
        """
        :param user_agent:
        :return:
        Establecer el User Agent con el que queremos navegar
        """
        self.user_agent = user_agent

    def set_lista_blanca(self, lista=[]):
        """
        :param lista:
        :return:
        Establecer una lista blanca de elementos que serán unicamente los que descarguen
        """
        self.lista_blanca = lista

    def set_ruta_raiz_descarga(self, ruta_raiz: str):
        """
        :param ruta_raiz:
        :return: ruta_raiz
        Establece la Ruta raiz donde se descargaran todas las páginas de la Web que hemos seleccionado,
        por defecto se descargará en ./datos/
        """
        self.ruta_raiz_descarga = ruta_raiz

    def set_numero_paginas_descargar(self, numero_max_descargas: int = -1):
        """
        :return:
        Establece el número máximo de páginas descargadas que cumplan criterios de listablanca
        a partir de la superacion de dicho número de páginas descargadas para el crawler
        """
        self.limite_paginas_descargadas = numero_max_descargas

    def download_url(self, url: str):
        """
        :param self:
        :param url:
        :return:
        Guarda el conrenido de la url en la ruta especificada.
        """
        headers = {'User-agent': self.user_agent}
        return requests.get(url, headers=headers).text

    def get_linked_urls(self, url: str, html: str):
        """
        :param self:
        :param url:
        :param html:
        :return:
        Obtiene todos los enlaces de la página para irlos recorriendo y se los pasa al metood para añadirlos
        en la cola de descargas.
        """
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path


    def add_url_to_visit(self, url: str):
        """
        :param self:
        :param url:
        :return:
        Añade la url en la cola de descargas del crawler
        """
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url: str, folder: str):
        """
        :param self:
        :param url:
        :param folder:
        :return:
        Es la araña que va reorriendo los enlaces que hay en el portal configurado.
        """
        headers = {'User-agent': self.user_agent}
        parseo = urlparse(url)
        descargamos = False

        for elemento in self.lista_blanca:
            if elemento in parseo.path:
                descargamos = True

        if self.lista_blanca == []:
            descargamos = True

        fichero = os.path.join(self.ruta_raiz_descarga + '/' + folder + parseo.path)
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
        try:
            if descargamos == True:
                os.makedirs(os.path.dirname(fichero), exist_ok=True)
        except FileExistsError:
            logging.info('El fichero ya existe')
        try:
            if descargamos == True:
                with open(fichero, "w") as f:
                    f.write(html)
        except IsADirectoryError:
            logging.info('Es un Directorio')
        except NotADirectoryError:
            logging.info('No es un directorio')
        except:
            logging.info('No se reconoce el formato de Descarga')
        finally:
            if descargamos == True:
                self.limite_paginas_descargadas = self.limite_paginas_descargadas -1
                logging.info(f'Descontamos el contador de paginas {self.limite_paginas_descargadas}')
                if(self.limite_paginas_descargadas == 0):
                    logging.info(f'Finalizamos por alcanzar el contador de paginas maxima')
                    self.urls_to_visit = []


    def run(self):
        """
        :param self:
        :return:
        Ejecuta la araña.
        """

        logging.info(f'El agente usado es: {self.user_agent}')

        number = 0
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            folder = self.folder
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url, folder)
            except Exception as e:
                logging.info(f'Failed to crawl: {url}')
                logging.info(e)
            except requests.exceptions.MissingSchema:
                logging.info(f'URL Incorrecta: {url}')
            finally:
                self.visited_urls.append(url)
            number += 1
