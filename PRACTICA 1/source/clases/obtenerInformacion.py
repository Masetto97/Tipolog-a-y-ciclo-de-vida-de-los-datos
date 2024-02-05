# Imports Seccion
import os
import locale
import logging
from bs4 import BeautifulSoup
import pandas as pd
import glob


class obtenerInformacion:
    """
    Clase para obtener la informacion previamente descargada por el crawler/spider.
    """
    os.environ["PYTHONIOENCODING"] = "utf-8"
    myLocale = locale.setlocale(category=locale.LC_ALL, locale="es_ES.UTF-8")

    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.INFO)

    def __init__(self, folder_wallapop: str ='datos/wallapop/'):
        """
        :param folder_wallapop:
        Constructor de la claee recibe como parámetro la ruta base de descarga del crawler que nos
        interesa explorar.
        """
        logging.info(f'Iniciando la Clase para Obtener Informacion')
        logging.info(f'Obtenemos Informacion de: {folder_wallapop}')
        self.folder_wallapop = folder_wallapop


    def set_ruta_items(self, folder: str ='wallapop/item'):
        """
        :param folder:
        :return:
        Establece la ruta donde están los HTMLS que queremos parsear con beautifulsoup
        """
        path_items_wallapop = os.path.join(self.folder_wallapop, folder)
        logging.info(f'Establecemos la ruta de Items de wallapop en: {path_items_wallapop}')
        self.path_items_wallapop = path_items_wallapop

    def procesar_items(self) -> pd.DataFrame:
        """
        :return:
        Procesamos los items (es decir la ruta con los htms a parsear)
        """
        Precio = []
        Producto = []
        Detalle_Producto = []
        v_Hash = []
        url = []
        v_usuario = []
        v_Ubicacion = []
        v_Fecha = []
        v_Visitas = []
        v_productos_usuario = []

        logging.info(f'Extraemos informacion de: {self.path_items_wallapop}')

        for fichero in glob.glob(os.path.join(self.path_items_wallapop, '*')):
            logging.info(f'Procesamos: {fichero}')
            with open(fichero, 'r', encoding="ISO-8859-1") as f:
                data = f.read()
            f.close()

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(data, "html.parser")

            # Obtenemos todos los divs donde están las entradas
            entradas_producto_tit = html.find_all('div', {'class': 'card-product-detail-top'})

            for i, entrada in enumerate(entradas_producto_tit):
                detalle_precio = detalle_producto = detalle_ampliado = Hashs = Ubicacion = Fecha = 'Ninguno'
                Visitas = 0

                try:
                    detalle_precio = entrada.find('div', {'class': 'card-product-price-info-wrapper'}).getText()
                    detalle_producto = entrada.find('h1', {'id': 'item-detail-title'}).getText()
                    detalle_ampliado = entrada.find('p', {'class': 'card-product-detail-description'}).getText()
                    Hashs = entrada.find('div', {'class': 'Hashtag Hashtag--odd'}).getText()
                    Ubicacion = entrada.find('div', {'class': 'card-product-detail-location'}).getText()
                    Fecha =  entrada.find('div', {'class': 'card-product-detail-user-stats-published'}).getText()
                    Visitas = entrada.find_all('div', {'class': 'card-product-detail-user-stats-right'}).getText()

                except:
                    pass


            # Obtenemos todos los divs donde están las entradas
            user = html.find_all('div', {'class': 'card-user-detail-info'})
            unico_usuario = set()

            for i, entrada in enumerate(user):
                try:
                    unico_usuario.add(entrada.find('h2', {'class': 'card-user-detail-name'}).getText())
                except:
                    pass

            v_usuario.append(str(unico_usuario).replace("{'", "").replace("'}", ""))

            # Añadimos el precio del articulo
            Precio.append(detalle_precio)
            Producto.append(detalle_producto)
            Detalle_Producto.append(detalle_ampliado)
            v_Hash.append(Hashs)
            v_Ubicacion.append(Ubicacion)
            v_Fecha.append(Fecha)
            v_Visitas.append(Visitas)

            try:
                meta_url = html.find('meta', {'property': 'og:url'})
                url.append(meta_url['content'])
            except:
                url.append('Ninguna')

        df_wallapop = pd.DataFrame({'Producto': Producto, 'Usuario': v_usuario, 'Detalle Producto': Detalle_Producto,
                                    'Precio': Precio, 'Ubicacion' : v_Ubicacion, 'Fecha': v_Fecha,
                                    'Visitas': v_Visitas, 'Hash': v_Hash, 'url': url})
        return df_wallapop

