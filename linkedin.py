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
        if not ostype:
            raise ValueError("An OS type must be specified.")

        script_directory = os.path.dirname(os.path.realpath(__file__))

        chrome_driver_path = os.path.join(script_directory, f'chromedriver-{ostype}', 'chromedriver')

        options = webdriver.ChromeOptions()

        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def login(self):
        url = "https://www.linkedin.com/login"
        if self.driver is None:
            raise Exception("Driver has not been initialized.")
        self.driver.get(url)

    def scrape(self, query, max_pages=1):
        base_url = "https://www.linkedin.com/search/results/people/?keywords="
        if self.driver is None:
            raise Exception("Driver has not been initialized.")

        all_contacts = []  # Store contacts as dictionaries

        for page in range(1, max_pages + 1):
            self.driver.get(f"{base_url}{query}&page={page}")

            xpath_expression = "//a[contains(@class,'app-aware-link') and contains(@class, 'scale-down') and not(contains(@href, 'headless'))]"
            elements = self.driver.find_elements(By.XPATH, xpath_expression)

            profile_urls = [element.get_attribute('href').split("?")[0] + "/overlay/contact-info/" for element in elements]

            for profile_url in profile_urls:
                try:
                    self.driver.get(profile_url)
                    time.sleep(1)  # Wait for page elements to load
                    
                    # Extracting title
                    title_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "text-body-medium break-words")]')
                    title = title_elements[0].text if title_elements else "No title available"
                    
                    # Extracting email
                    email_elements = self.driver.find_elements(By.XPATH, '//a[contains(@href, "mailto:")]')
                    for email_element in email_elements:
                        email_address = email_element.get_attribute('href').replace('mailto:', '')
                        contact = {"title": title, "email": email_address}
                        all_contacts.append(contact)
                except Exception as e:
                    print(f"An error occurred while trying to fetch the profile: {e}")
                time.sleep(1)

        if not all_contacts:
            return "None"
        else:
            # Optionally, filter duplicates based on email addresses if necessary
            unique_contacts = {contact['email']: contact for contact in all_contacts}.values()
            return list(unique_contacts)


    def wait(self):
        input("Press enter to continue...")

    def end(self):
        if self.driver:
            for i in range(5, 0, -1):
                print(f"Session terminating in {i}", end='\r', flush=True)
                time.sleep(1)
            self.driver.quit()
            self.driver = None