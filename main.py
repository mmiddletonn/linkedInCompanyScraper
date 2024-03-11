import csv
import os_detection
import linkedin

platform = os_detection.platform
session = linkedin.session(platform)

employee_emails = {}

with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for company in row:
            # print(company)
            employee_emails[company] = session.scrape(company)

print(employee_emails)

session.end()