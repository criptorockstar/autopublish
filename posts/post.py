import os
import re
import sys
import time
import csv
import threading
from translations import I18n
from datetime import datetime, timedelta
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Post:
    def __init__(self, driver, config) -> None:
        self.driver = driver

        self.i18n = I18n()
        self.config = config
        self.console = Console()
       
        # Stoping signal
        self.stop = 0

        # Internal clock
        self.current_time = None

        # DateTime trigger
        self.trigger = None
        
        # Instance of posts
        self.posts = None


    def start(self):
        def timer():
            while True: # Fetch current DateTime in a loop
                actual_date = datetime.utcnow()
                self.current_time = datetime.strptime(actual_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                
        self.console.print(self.i18n.translate(self.config.get_locale(), "post.inner_clock"), style="bold yellow")
        # Start time thread
        timer = threading.Thread(target=timer)
        timer.start()


        self.console.print(self.i18n.translate(self.config.get_locale(), "post.loading_posts"), style="bold yellow")
        # Wait till current_time is initialized
        while True:
            if self.current_time is not None:
                self.initialize()
                break
        
        while self.posts:
            self.initialize()

    
    def initialize(self):
        # Fetch posts if empty
        if self.posts is None and self.stop == 0:
            self.posts = self.fetch()
            self.stop = 1
        
         # Extract the first row
        first_row = self.posts.pop(0) if self.posts else None

        # Check if the file is empty
        if first_row is None:
            self.console.print(self.i18n.translate(self.config.get_locale(), "post.empty_records"), style="bold red")
            self.driver.quit()
            quit()
        
        # Print keys and values of the first row
        for key, value in first_row.items():
            print(f"{key}: {value}") 


    def fetch(self):
        posts = './posts.csv'
        all_rows = []

        if not os.path.isfile(posts):
            self.console.print(self.i18n.translate(self.config.get_locale(), "post.empty_records"), style="bold red")
            self.driver.quit()
            quit()
        
        # Open posts file as read only
        with open(posts, 'r', newline='', encoding='utf-8') as file:
            # Create a CSV object
            reader = csv.DictReader(file)

            # Almacenar todas las filas en la lista
            all_rows = list(reader)

        return all_rows
