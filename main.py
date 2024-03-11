import csv
import os_detection
import linkedin

# Initialize the platform and session
platform = os_detection.platform
session = linkedin.session(platform)

employee_emails = {}
with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for company in row:
            employee_emails[company] = session.scrape(company, 10)

# Path to the CSV file
csv_file_path = 'employee_emails.csv'

# Write the employee emails to the CSV file
with open(csv_file_path, mode='w', newline='') as csvfile:
    fieldnames = ['Company', 'Title', 'Email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write employee information for each company
    for company, employees in employee_emails.items():
        for employee in employees:
            writer.writerow({'Company': company, 'Title': employee['title'], 'Email': employee['email']})

# End the sessions
session.end()

print(f"Employee emails have been saved to '{csv_file_path}'.")