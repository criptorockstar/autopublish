import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.locale = os.getenv("LANGUAGE")
        self.headless = os.getenv("HEADLESS")
   
        self.options = [
            ("detach", True),
            ("--disable-notifications", None),
            ("--disable-infobars", None),
            ("--disable-popup-blocking", None),
            ("--ignore-certificate-errors", None),
            ('--disable-extensions', None),
            ("--disable-infobars", None),
            ("--lang=en", None)
        ]

        self.sizes = (640, 480)


    def get_sizes(self):
        return self.sizes


    def get_options(self):
        return self.options, self.sizes


    def get_locale(self):
        return self.locale


    def get_headless(self):
        return self.headless


    def set_locale(self, locale):
        # Read the .env file
        env_path = ".env"
        value = "en" if locale == 'en' else "es"

        with open(env_path, "r") as env_file:
            lines = env_file.readlines()

        # Modify the value of LANGUAGE
        for i, line in enumerate(lines):
            if line.startswith("LANGUAGE="):
                lines[i] = f"LANGUAGE={value}\n"
                break

        # Write the modified lines to .env
        with open(env_path, "w") as env_file:
            env_file.writelines(lines)

        # update the attribute on the instance
        self.locale = value 


    def set_headless(self, headless):
        # Read the .env file
        env_path = ".env"
        value = headless

        with open(env_path, "r") as env_file:
            lines = env_file.readlines()

        # Modify the value of HEADLESS
        for i, line in enumerate(lines):
            if line.startswith("HEADLESS="):
                lines[i] = f"HEADLESS={value}\n"
                break

        # Write the modified lines to .env
        with open(env_path, "w") as env_file:
            env_file.writelines(lines)

        # Update the attribute on the instance
        self.headless = value
