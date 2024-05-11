import os
import csv
import re
from datetime import datetime

def extract_info_from_csv(file_path):
    total_amount = 0.0
    date_str = ""
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                joined_row = ' '.join(row)
                print(f"Processing row: {joined_row}")  # Debug print
                
                if not date_str:
                    date_match = re.search(r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{2} (AM|PM|am|pm)', joined_row)
                    if date_match:
                        date_str = datetime.strptime(date_match.group(), "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d")
                        print(f"Date found: {date_str}")  # Debug print

                # Regex to capture the total; adjusted for potential formats
                total_match = re.search(r'\bTotal\b.*?\$([\d,]+\.\d{2})', joined_row)
                if total_match:
                    total_str = total_match.group(1).replace(',', '')
                    total_amount = float(total_str)
                    print(f"Total amount captured: {total_amount}")  # Debug print
                    break  # Stop processing once total is found

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    return total_amount, date_str

def calculate_totals(directory_path):
    grand_total = 0.0
    totals_by_date = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str = extract_info_from_csv(file_path)
            if date_str:
                grand_total += total
                if date_str in totals_by_date:
                    totals_by_date[date_str] += total
                else:
                    totals_by_date[date_str] = total

    return grand_total, totals_by_date

def save_to_csv(grand_total, totals_by_date, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Total'])
        for date, total in sorted(totals_by_date.items()):
            writer.writerow([date, f"${total:.2f}"])
        writer.writerow(['Grand Total', f"${grand_total:.2f}"])

# Execution
directory_path = 'receipts'
output_csv_file = 'totals_summary.csv'
grand_total, totals_by_date = calculate_totals(directory_path)
print(f"Grand Total: ${grand_total:.2f}")
save_to_csv(grand_total, totals_by_date, output_csv_file)
