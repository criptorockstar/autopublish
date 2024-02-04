import os.path
import sys
import inquirer
from rich import print
from pytz import all_timezones
from config import Config
from translations import I18n
from rich.console import Console
from posts import Post
from session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self) -> None:
        self.console = Console()
        self.config = Config()
        self.i18n = I18n()


    def load(self):
        options, sizes = self.config.get_options()
        chrome_options = webdriver.ChromeOptions()

        for option, value in options:
            if value is not None:
                chrome_options.add_argument(f"{option}={value}")
            else:
                chrome_options.add_argument(option)

        if self.config.get_headless() == 1:
            chrome_options.add_argument('--headless')

        # For testing purposes
        chrome_options.add_experimental_option("detach", True)
        # For testing purposes
        driver = webdriver.Chrome(options=chrome_options)

        return driver


    def configure(self):
        def set_language(): 
            questions = [
                inquirer.List('language',
                              message='Choose your Language:',
                              choices=[
                                  ('English', 'en'),
                                  ('Español', 'es')
                              ],
                              default='1',  # Default choice
                              ),
            ]
            
            answers = inquirer.prompt(questions)
            language = answers['language']

            # Set language
            self.config.set_locale(language)
         
       
        def set_headless():
            # Get translated message
            set_headless = self.i18n.translate(self.config.get_locale(), "main.headless")
            choose = self.i18n.translate(self.config.get_locale(), "main.choose")

            questions = [
                inquirer.List('choice',
                              message=set_headless,
                              choices=[choose, 'No'],
                              ),
                ]

            answers = inquirer.prompt(questions)
            choice = answers['choice'] == choose
            
            # Set headless choice
            self.config.set_headless(choice)

        # Set language
        set_language()
         
        # Set Headless
        headless = set_headless()

    
    def start(self):
        # Get configuration
        locale = self.config.get_locale()
        headless = self.config.get_headless()
        
        # Check if values are not empty
        if locale == "" and headless == "":
            self.configure()
        
        # Print user settings
        self.console.print("Settings", style="bold green")
        print(self.i18n.translate(self.config.get_locale(), "main.language"), locale)
        print("Headless:", headless == 1)
        
        # Offer reconfigure options
        reconfigure = input("\nReconfigure? (y/n): ")

        if reconfigure.lower() == 'y':
            self.configure()
        elif reconfigure.lower() != 'n':
            self.console.print("invalid response", style="bold red")

        # Load user's preferences'
        self.console.print(self.i18n.translate(self.config.get_locale(), "main.loading_preferences"), style="bold green")
        driver = self.load()

        # Load external classes
        self.session = Session(driver, self.config)

        # Check if cookie exists 
        self.console.print(self.i18n.translate(self.config.get_locale(), "main.loading_cookies"), style="bold green")
        if not os.path.isfile("./session/cookies/cookie.pkl"):
            self.session.login()

        # Try to load session's cookie
        try:
            self.session.load()
        except:
            self.session.login()
 
  
if __name__=="__main__":
    bot = Bot() 
    bot.start()
