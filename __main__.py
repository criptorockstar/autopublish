import os.path
import sys
import inquirer
from pytz import all_timezones
from config import Config
from translations import Lang
from rich.console import Console
from posts import Post
from session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self) -> None:
        self.console = Console()
        self.options = Options()
        self.config = Config()
        self.lang = Lang()


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

            # Show chosen language
            chosen_language = 'en' if language == '1' else 'es'
        
            self.console.print(self.lang.translate(self.config.get_locale(), "main.set_language"), style='bold green')
       
        def set_continent(): 
            # Get translated continent names
            set_continent = self.lang.translate(self.config.get_locale(), "main.set_continent")
            europe = self.lang.translate(self.config.get_locale(), "main.europe")
            pacific = self.lang.translate(self.config.get_locale(), "main.pacific")
            
            # Continents
            questions = [
                inquirer.List('continent',
                              message=set_continent,
                              choices=['Africa', 'America', 'Asia', europe, pacific],
                              ),
            ]

            continent_answers = inquirer.prompt(questions)
            continent = continent_answers['continent']
            
            timezone = set_timezone(continent) 

        def set_timezone(continent):
            # Get trnaslated timezone names
            set_timezone = self.lang.translate(self.config.get_locale(), "main.set_timezone")
            
            # Get all timezones
            continent_timezones = [tz for tz in all_timezones if tz.startswith(continent)]
            
            questions = [
                inquirer.List('timezone',
                              message=set_timezone,
                              choices=continent_timezones,
                              ),
            ]
            
            answers = inquirer.prompt(questions)
            timezone = answers['timezone']
            
            self.config.set_timezone(timezone) 

        def set_headless():
            # Get translated message
            set_headless = self.lang.translate(self.config.get_locale(), "main.headless")
            choose = self.lang.translate(self.config.get_locale(), "main.choose")

            questions = [
                inquirer.List('choice',
                              message=set_headless,
                              choices=[choose, 'No'],
                              ),
                ]

            answers = inquirer.prompt(questions)
            choice = answers['choice'] == choose
            
            self.config.set_headless(choice)

        # Set language
        set_language()
        
        # Set timezone
        continent = set_continent()
        
        # Set Headless
        headless = set_headless()

    
    def start(self):
        locale = self.config.get_locale()
        timezone = self.config.get_timezone()
        headless = self.config.get_headless()
        print(locale)
        print(timezone)
        print(headless == 1)

    '''
    def start(self):
        # Check if session's cookie exists
        if not os.path.isfile("./session/cookies/cookies.pkl"):
            self.session.login()

        # Try to load session's cookie
        try:
            self.session.load()
        except:
            self.session.login()

        # Execution start
        self.post.start()
    '''

if __name__=="__main__":
    bot = Bot()
    bot.start()
