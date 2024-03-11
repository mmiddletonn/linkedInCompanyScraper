import os_detection
import linkedin

platform = os_detection.platform
session = linkedin.session(platform)

companies = ["google", "apple"]
employee_emails = {}

for company in companies:
    employee_emails[f"{company}"] = session.scrape(f"{company}")

print(employee_emails)

session.end()