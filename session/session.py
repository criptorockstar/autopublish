import os
import getpass
import pickle
from translations import I18n
from config import Config
from datetime import datetime
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Session:
    def __init__(self, driver, config) -> None:
        self.driver = driver
        self.console = Console()

        # Translations
        self.i18n = I18n()
        self.config = config


    def login(self):
        self.driver.get(f"https://www.facebook.com/?locale=en&login")

        user = self.driver.find_element(By.CSS_SELECTOR, 'input[id="email"]')
        password = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pass"]')
        submit = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        # Ask user's credentials
        self.console.print(self.i18n.translate(self.config.get_locale(), "session.credentials"), style="bold yellow")
        user.send_keys(input(self.i18n.translate(self.config.get_locale(), "session.email")))
        password.send_keys(getpass.getpass(self.i18n.translate(self.config.get_locale(), "session.password")))
        submit.click()

        # Wait till the URL changes
        WebDriverWait(self.driver, 10).until(
            EC.url_changes("https://www.facebook.com/?locale=en&login")
        ) 

        # Navigate to english's default dashboard
        self.driver.get("https://www.facebook.com/?locale=en&sk=welcome")

        # Check if a dashboard element is found
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create"]'))
            )
        except:
            self.console.print(self.i18n.translate(self.config.get_locale(), "session.wrong_credentials"), style="bold red")
            self.driver.quit()
            quit()

        self.console.print(self.i18n.translate(self.config.get_locale(), "session.success"), style="bold green")
        self.console.print(self.i18n.translate(self.config.get_locale(), "session.storing_cookies"), style="bold yellow")
        
        # Get browse's cookies
        cookies = self.driver.get_cookies()

        # Store cookies
        with open("./session/cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)


    def load(self): 
        # Load cookies
        with open("./session/cookies.pkl", "rb") as file:
            cookies = pickle.load(file)

        # Navigate to login screen
        self.driver.get("https://www.facebook.com/?locale=en&login")

        # Set cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        
        # Navigate to dashboard
        self.driver.get("https://www.facebook.com/?locale=en&sk=welcome")

        # Check if login was successful->looking for a dashboard's element
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create"]'))
            )
        except TimeoutException:
            os.remove("./session/cookies.pkl")
            raise Exception()
