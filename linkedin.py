import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class session:
    def __init__(self, ostype):
        self.driver = None
        self.init_driver(ostype)
        self.login()
        self.wait()

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


    def scrape(self, query, max_pages=2):
        base_url = "https://www.linkedin.com/search/results/people/?keywords="
        if self.driver is None:
            raise Exception("Driver has not been initialized.")

        all_email_addresses = []

        for page in range(1, max_pages + 1):
            self.driver.get(f"{base_url}{query}&page={page}")
            
            xpath_expression = "//a[contains(@class,'app-aware-link') and contains(@class, 'scale-down') and not(contains(@href, 'headless'))]"
            elements = self.driver.find_elements(By.XPATH, xpath_expression)
            
            profile_urls = [element.get_attribute('href').split("?")[0] + "/overlay/contact-info/" for element in elements]

            for profile_url in profile_urls:
                try:
                    self.driver.get(profile_url)
                    time.sleep(1)
                    email_elements = self.driver.find_elements(By.XPATH, '//a[contains(@href, "mailto:")]')
                    for email_element in email_elements:
                        email_address = email_element.get_attribute('href').replace('mailto:', '')
                        all_email_addresses.append(email_address)
                except Exception as e:
                    print(f"An error occurred while trying to fetch the profile: {e}")
                time.sleep(1)
        
        if not all_email_addresses:
            return "None"
        else:
            unique_email_addresses = list(set(all_email_addresses))
            return str(unique_email_addresses)


    def wait(self):
        input("Press enter to continue...")

    def end(self):
        if self.driver:
            for i in range(5, 0, -1):
                print(f"Session terminating in {i}", end='\r', flush=True)
                time.sleep(1)
            self.driver.quit()
            self.driver = None