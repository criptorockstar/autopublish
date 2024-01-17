import getpass
import pickle
from rich import print
from rich.console import Console
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Session:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.console = Console()


    def login(self):
        self.driver.get("https://www.facebook.com/login")

        user = self.driver.find_element('xpath', '//*[@id="email"]')
        password = self.driver.find_element('xpath', '//*[@id="pass"]')
        submit = self.driver.find_element('xpath', '//*[@id="loginbutton"]')

        # Pedir credenciales
        self.console.print("Ingresa las credenciales de la cuenta.", style="bold yellow")
        user.send_keys(input("Correo electronico o numero de telefono: "))
        password.send_keys(getpass.getpass("Contraseña: "))
        submit.click()

        # Esperar a que la URL cambie
        WebDriverWait(self.driver, 10).until(
            EC.url_changes("https://www.facebook.com/login")
        )

        # Verificar la nueva URL
        if "https://www.facebook.com/?sk=welcome" in self.driver.current_url:
            self.console.print("Inicio de sesión exitoso.", style="bold green")
            cookies = self.driver.get_cookies()

            # Guardar cookies de sesion
            with open("./session/cookies/cookies.pkl", "wb") as file:
                pickle.dump(cookies, file)
            
            # Cargar cookies
            self.load()
        else:
            self.console.print("Error al iniciar sesión.", style="bold red")
            self.driver.quit()


    def load(self):
        with open("./session/cookies/cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        
        # Abrir una página web y establecer las cookies
        self.driver.get("https://www.facebook.com/login")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get("https://www.facebook.com/?sk=welcome")