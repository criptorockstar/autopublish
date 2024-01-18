import os.path
from posts import Post
from session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-notifications")
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')

        # Muestra el tema oscuro de chrome
        self.options.add_argument('--force-dark-mode')
        
        self.driver = webdriver.Chrome(options=self.options)
        self.post = Post(self.driver)
        self.session = Session(self.driver)


    def start(self):
        if os.path.isfile("./session/cookies/cookies.pkl"):
            self.session.load()
            self.post.load()
        else:
            self.session.login()


if __name__=="__main__":
    bot = Bot()
    bot.start()