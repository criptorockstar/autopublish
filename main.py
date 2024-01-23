import os.path
from posts import Post
from session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Bot:
    def __init__(self, timezone) -> None:
        self.timezone = timezone
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
        self.driver.set_window_size(640, 480)
        self.post = Post(self.driver, self.timezone)
        self.session = Session(self.driver)


    def start(self):
        if os.path.isfile("./session/cookies/cookies.pkl"):
            self.session.load()
            #self.post.start() #habilitar al terminar las pruebas

            # para pruebas / borrar al terminar las pruebas
            df = self.post.fetch()
            self.post.load()
            self.post.publish(df)
            # para pruebas / borrar al terminar las pruebas
        else:
            self.session.login()


if __name__=="__main__":
    zona = "America/Montevideo" #Ajusta la zona horaria
    bot = Bot(zona)
    bot.start()