import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class session:
    def __init__(self, ostype):
        self.driver = None
        self.init_driver(ostype)

    def init_driver(self, ostype):
        # Validate the OS type argument
        if not ostype:
            raise ValueError("An OS type must be specified.")

        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to ChromeDriver dynamically based on the OS type
        chrome_driver_path = os.path.join(script_directory, f'chromedriver-{ostype}', 'chromedriver')

        # Set up the ChromeDriver options
        options = webdriver.ChromeOptions()
        # Add any Chrome options if needed

        # Set up the service with the dynamically constructed path
        service = Service(executable_path=chrome_driver_path)

        # Initialize the WebDriver instance using the specified ChromeDriver
        self.driver = webdriver.Chrome(service=service, options=options)

    def login(self):
        url = "https://www.linkedin.com/login"
        if self.driver is None:
            raise Exception("Driver has not been initialized.")
        self.driver.get(url)

    def search(self, query):
        url = "https://www.linkedin.com/search/results/all/?keywords="
        if self.driver is None:
            raise Exception("Driver has not been initialized.")
        self.driver.get(url + query)

    def wait(self):
        input("Press enter to continue...")

    def end(self):
        if self.driver:
            self.driver.quit()
            self.driver = None