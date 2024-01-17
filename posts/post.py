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
        plus = self.driver.find_element('xpath', '//*[@id="mount_0_0_uZ"]/div/div[1]/div/div[2]/div[5]/div[1]/div[3]/div[2]/span/div')
        plus.click()

        # lee los posts dentro del archivo CSV
        self.fetch()


    def fetch(self):
        posts = []
        archivo = './posts.csv'

        # Abre el archivo CSV y lee línea por línea
        with open(archivo, 'r') as file:
            lines = file.readlines()
            post = {}
            for line in lines:
                line = line.strip()
                if line.startswith('contenido: '):
                    post['contenido'] = line[len('contenido: '):]
                elif line.startswith('imagen: '):
                    post['imagen'] = line[len('imagen: '):]
                    # Agrega el post a la lista y reinicializa 
                    # el diccionario para el próximo post
                    posts.append(post)
                    post = {}

        # Muestra los posts
        for i, post in enumerate(posts, 1):
            print(f"Post {i}:")
            print(f"Contenido: {post.get('contenido')}")
            print(f"Imagen: {post.get('imagen')}")
            print("\n")


    def publish(self):
        pass