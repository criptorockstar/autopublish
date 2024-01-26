import os
import re
import sys
import pytz
import time
import csv
import threading
from datetime import datetime, timedelta
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Post:
    def __init__(self, driver, timezone, lang, t) -> None:
        self.driver = driver
        self.console = Console()
        
        # Users' settings
        self.timezone = timezone
        self.lang = lang
        self.t = t

        # Internal clock
        self.current_time = None

        # DateTime trigger
        self.trigger = None

        # Post's data
        self.content = None
        self.image = None


    def start(self):
        def timer():
            while True: # Fetch current DateTime in a loop
                zona = pytz.timezone(self.timezone)
                utc_time = datetime.utcnow()
                actual_date = utc_time.replace(tzinfo=pytz.utc).astimezone(zona)
                self.current_time = datetime.strptime(actual_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        # Start time thread
        timer = threading.Thread(target=timer)
        timer.start()

        # Wait till current_time is initialized
        while True:
            if self.current_time is not None:
                self.initialize()
                break

        # Procced with posting functions
        while self.content:
            # Check if event is triggered
            if self.current_time < self.trigger:
                continue
                
            # Publish the scheduled post
            self.publish()

            # initialize new post
            self.initialize()


    def initialize(self):
        data = self.fetch()
        
        # Iterate and filter values
        self.content = data[0]
        self.image = data[1]
        postime = data[2]

        match = re.search(r'(\d+)([a-zA-Z])$', postime)
        if not match: # verify postime format
            self.console.print(self.t(self.lang, "post.invalid_timeformat"), style="bold red")
            self.driver.quit()
            sys.exit(1)

        # Diasemble postime into number and value
        timenumber = int(match.group(1))
        timevalue = match.group(2)

        # Checks if values has valid formats
        if timevalue != 's' and timevalue != 'm' and timevalue != 'h':
            self.console.print(self.t(self.lang, "post.invalid_timevalues"), style="bold red")
            self.driver.quit()
            sys.exit(1)
        
        # Set trigger
        match timevalue:
            case 's':
                target = self.current_time + timedelta(seconds=timenumber)
                self.trigger = target
            case 'm':
                target = self.current_time + timedelta(minutes=timenumber)
                self.trigger = target
            case 'h':
                target = self.current_time + timedelta(hours=timenumber)
                self.trigger = target

        
    def load(self):
        # Navigate to dashboard
        self.driver.get("https://www.facebook.com/?locale=en&sk=welcome")
        
        # Clicks over '+' button
        plus = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create"]'))
        )
        plus.click()

        # Clicke over "Post" item
        boton_post = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Post"]'))
        )
        boton_post.click()


    def fetch(self):
        posts = './posts.csv'
        data = []

        # Open posts file as read only
        with open(posts, 'r', newline='', encoding='utf-8') as file:
            # Create a CSV object
            reader = csv.reader(file)

            # Read the first row (header)
            header = next(reader)

            # Iterate over the first row and append to data
            for row in reader:
                data.append(row)
        
        # Check is data is not empty
        if not data:
            self.console.print(self.t(self.lang, "post.empty_records"), style="bold red")
            self.driver.quit()
            sys.exit(1)
    
        # Delete the first row from the file
        with open(posts, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Rewrite the header and the data without the first row
            writer.writerow(header)
            writer.writerows(data[1:])

        return data[0] if len(data) > 0 else []


    def publish(self):
        # Navigate to post's interface
        self.load()

        # @Input -> Post's content
        content = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@aria-label, "What\'s on your mind,")]'))
        )
        content.send_keys(self.content)

        # Button -> attach item
        menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Add to your post"]'))
        )
        menu.click()

        # Item -> Foto/Video
        picture = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Photo/video"]'))
        )
        picture.click()
        
        # Upload image
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        # Get full path from image's file
        image_path = os.path.expanduser(self.image)

        # Send the full path from image to input
        file_input.send_keys(image_path)

        # Submit -> publish
        submit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Post"]'))
        )
        
        # Change visibility
        self.driver.execute_script("arguments[0].style.display = 'block';", submit)

        # Wait to changes to be completed
        time.sleep(3)

        # Simulate a click using JavaScript
        self.driver.execute_script("arguments[0].click();", submit)
