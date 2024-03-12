import csv
import os_detection
import linkedin

# Initialize the platform and session
platform = os_detection.platform
session = linkedin.session(platform)

companies = ["google", "apple"]

for company in companies:
    session.scrape(f"{company}")

# with open('data.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         for company in row:
#             session.scrape(company, 10)

# End the sessions
session.end()