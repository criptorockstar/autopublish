import os.path
from dotenv import load_dotenv
from posts import Post
from session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyi18n import PyI18n

# Load configuration settings
load_dotenv()


class Bot:
    def __init__(self) -> None:
        # Set user's settings
        self.timezone = os.getenv("ZONA")
        self.lang = os.getenv("LOCALE")
        self.options = Options()

        # Set locales
        i18n = PyI18n(("en", "es"), load_path="translations/")
        self.t: callable = i18n.gettext

        # Chromedriver's options
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-notifications")
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        
        # Set the driver's default language to english
        self.options.add_argument("--lang=en")

        # Run in headless mode
        self.options.add_argument('--headless')
        
        # Start driver
        self.driver = webdriver.Chrome(options=self.options)
        
        # Set driver's window size
        self.driver.set_window_size(640, 480)
        
        # Load external class
        self.post = Post(self.driver, self.timezone, self.lang, self.t)
        self.session = Session(self.driver, self.lang, self.t)


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


if __name__=="__main__":
    bot = Bot()
    bot.start()