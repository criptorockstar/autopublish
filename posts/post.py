import re
import threading
import pytz
import pandas as pd
from datetime import datetime
from rich import print
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Post:
    def __init__(self, driver, timezone) -> None:
        self.driver = driver
        self.new_timezone = pytz.timezone(timezone)


    def start(self):
        posts = None

        def calculate():
            df = self.fetch()
            
            if df is None: # verificamos que el archivo tenga posts
                print("El archivo posts.csv esta vacio")
                self.driver.quit()

            # Seleccionamos el primer post
            post_item = df.iloc[0]
            tiempo = post_item.tiempo
            
            ''' @Filtramos por:
            (s)egundos
            (m)inutos
            (h)oras
              El primer valor debe ser numerico y el segundo una letra
              de las indicadas arriba: por ejemplo 30s corresponde a 30 segundos 
            '''
            match = re.search(r'(\d+)([a-zA-Z])$', tiempo)
            if not match: # verificamos que el tiempo tenga el formato esperado
                print("El tiempo no tiene un formato valido.")
                self.driver.quit()

            # verificamos que sea uno de los 3 valores mencionados
            if indicador is not 's' and indicador is not 'm' and indicador is not 'h':
                print("Los valores aceptados con: (s)egundo, (m)inutos, (h)oras.")
                self.driver.quit()

            numero = int(match.group(1))
            indicador = match.group(2)

            
            

        calculate()


    def load(self):
        self.driver.get("https://www.facebook.com/?sk=welcome")
        
        # Esperar hasta que el botón '+' sea visible
        plus = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Crear"]'))
        )
        plus.click()

        boton_post = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Publicación"]'))
        )
        boton_post.click()


    def fetch(self):
        archivo = './posts.csv'
        df = pd.read_csv(archivo)

        return df


    def publish(self, df):
        # Ruta de una imagen de prueba
        image_path = "/home/criptorockstar/Imágenes/gameover01.jpg"

        # @Input -> contenido del post
        content = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@aria-label, "¿Qué estás pensando,")]'))
        )
        content.send_keys("Contenido")

        ''' Obteniendo el input["file"]'''
        # Boton -> adjuntar elementos
        menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Agregar a tu publicación"]'))
        )
        menu.click()

        # Item -> Foto/Video
        picture = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Foto/video"]'))
        )
        picture.click()

        # Item -> agregar fotos/videos
        picture_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Agregar fotos/videos"]'))
        )
        picture_button.click()
        
        ''' Al gatillar el evento de insertar imagen aparece
        el input["file"] oculto en el D.O.M el cual podemos'''
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(image_path)

        # Submit -> Publicar