import pandas as pd
from rich import print
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Post:
    def __init__(self, driver) -> None:
        self.driver = driver


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

        # lee los posts dentro del archivo CSV
        self.fetch()


    def fetch(self):
        archivo = './posts.csv'
        df = pd.read_csv(archivo)
        
        # Se procede a publicar pasando los posts como parametro
        self.publish(df)

    def publish(self, df):
        # Input
        content = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@aria-label, "¿Qué estás pensando,")]'))
        )
        content.send_keys("Contenido")
        
        # Menu para elegir que elementos adjuntar
        menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Agregar a tu publicación"]'))
        )
        menu.click()

        # Item Foto/Video
        picture = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Foto/video"]'))
        )
        picture.click()