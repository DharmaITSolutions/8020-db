import csv

# Read the original CSV and extract emails
with open('members_list.csv', 'r') as input_file:
    csv_reader = csv.DictReader(input_file)
    emails = [row['email'] for row in csv_reader if row['email']]  # Only get non-empty emails

# Write emails to new CSV
with open('mailing_list.csv', 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['email'])  # Header
    for email in emails:
        csv_writer.writerow([email])

print(f"Created mailing_list.csv with {len(emails)} email addresses") 