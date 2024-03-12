import os
import time
import csv
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

    def scrape(self, query, max_pages=1, filename='contacts.csv'):
        base_url = "https://www.linkedin.com/search/results/people/?keywords="
        if self.driver is None:
            raise Exception("Driver has not been initialized.")
        
        # Check if the CSV file exists and read existing contacts if it does
        existing_contacts = set()
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_contacts.add(row['email'])  # Assuming email is unique

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
                        if email_address not in existing_contacts:  # Skip if email exists
                            contact = {"title": title, "email": email_address}
                            # Write contact to CSV file
                            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                                writer = csv.DictWriter(file, fieldnames=['title', 'email'])
                                if file.tell() == 0:  # File is empty, write header
                                    writer.writeheader()
                                writer.writerow(contact)
                            existing_contacts.add(email_address)  # Add to set to avoid duplicates
                except Exception as e:
                    print(f"An error occurred while trying to fetch the profile: {e}")
                time.sleep(1)

    def wait(self):
        input("Press enter to continue...")

    def end(self):
        if self.driver:
            for i in range(5, 0, -1):
                print(f"Session terminating in {i}", end='\r', flush=True)
                time.sleep(1)
            self.driver.quit()
            self.driver = None