import re
import threading
import pytz
import pandas as pd
import time
from datetime import datetime, timedelta
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
        self.timezone = timezone
        self.current_time = None # fecha/hora actual: se actualiza cada segundo
        self.trigger = None # fecha:hora:minuto:segundo del proximo post
        self.posts = None
        self.item = None # contenido,imagen del proximo post


    def start(self):
        def timer():
            while True:
                zona = pytz.timezone(self.timezone)
                utc_time = datetime.utcnow()
                actual_date = utc_time.replace(tzinfo=pytz.utc).astimezone(zona)
                self.current_time = datetime.strptime(actual_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        # obtenemos el tiempo actual y lo actualizamos segundo a segundo
        timer = threading.Thread(target=timer)
        timer.start()

        # Esperamos a que timer() termine de procesar el valor inicial
        while True:
            if self.current_time is not None:
                self.calculate()
                break

        step = False
        while len(self.data) > 0:
            # cargamos la interfaz de publicacion
            self.load()

            # procesamos
            step = self.check()
            
            # esperamos hasta que se procese el post
            if step == False:
                continue

            # cuando se procesa el post eliminamos la fila correspondiente del archivo posts.csv
            self.data = self.data.drop(self.data.index[0])

            # calculamos el siguiente evento futuro
            self.calculate()

        # Cuando no queden posts por procesar imprimimos un mensaje
        print("El archivo posts.csv esta vacio, todos los posts fueron procesados.")
        self.driver.quit()


    def check(self):
        # se mantiene checkeando en loop hasta que se cumpla el evento
        while self.current_time < self.trigger:
            pass
        
        # cuando se cumple el evento devolvemos True
        return True


    def calculate(self):
        self.data = self.fetch()
        
        if self.data is None: # verificamos que el archivo tenga posts
            print("El archivo posts.csv esta vacio")
            self.driver.quit()

        # Seleccionamos el primer post
        post_item = self.data.iloc[0]
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

        # Filtramos el numero y el indicador de tiempo            
        numero = int(match.group(1))
        indicador = match.group(2)

        # verificamos que sea uno de los 3 valores mencionados
        if indicador != 's' and indicador != 'm' and indicador != 'h':
            print("Los valores aceptados con: (s)egundo, (m)inutos, (h)oras.")
            self.driver.quit()

        # calculamos cuando se dispara el evento
        match indicador:
            case 's':
                target = self.current_time + timedelta(seconds=numero)
                self.trigger = target
            case 'm':
                target = self.current_time + timedelta(minutes=numero)
                self.trigger = target
            case 'h':
                target = self.current_time + timedelta(hours=numero)
                self.trigger = target
            case _:
                print("verifique el formato de tiempo.")
                self.driver.quit()
        
        # guardamos los datos del post para usarlos cuando sea el momento
        self.item = post_item


    def load(self):
        self.driver.get("https://www.facebook.com/?sk=welcome")
        
        # Esperar hasta que el botón '+' sea visible
        plus = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Crear"]'))
        )
        plus.click()

        # Clickeamos el elemento "publicacion"
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
        submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Publicar"]'))
        )
        submit.click()
        '''
        funciona todo pero por alguna razon al hacer click en publicar no pasa nada
        '''
        # Haciendo clic mediante JavaScript
        #self.driver.execute_script("arguments[0].click();", submit)
        print("completado")