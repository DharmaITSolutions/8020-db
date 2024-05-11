import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt

def extract_totals_from_csv(file_path):
    """ Extract the total, date, and line items from the CSV file, ensuring accurate date extraction. """
    total_amount = 0.0
    date_str = ""
    line_items = {}
    processing_items = False  # Flag to start processing line items
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            
            for row in reader:
                if not row:
                    continue
                # Adjusted to find the invoice line more reliably
                if any("Invoice" in s for s in row):
                    # Assumes date and time immediately follow "Terminal"
                    for element in row:
                        if "Terminal" in element:
                            date_part = element.split('-')[1].strip()
                            # Properly parse the date assuming it follows "Terminal 13 - MM/DD/YYYY HH:MM pm"
                            try:
                                date_str = datetime.strptime(date_part, "%m/%d/%Y %H:%M %p").strftime("%Y-%m-%d")
                            except ValueError:
                                continue  # If date format is incorrect, skip
                            break  # Exit loop once date is found
                elif "UPC" in row[0] and "Price" in row[-1]:  # This is the header row
                    processing_items = True  # Start processing after this line
                elif processing_items and len(row) > 2 and row[0].isdigit():
                    try:
                        price = float(row[-1].replace('$', '').strip())
                        description = row[1].strip()
                        if description in line_items:
                            line_items[description] += price
                        else:
                            line_items[description] = price
                    except ValueError:
                        continue  # Skip lines that cannot be converted to float
                elif "Total" in row[0]:
                    total_amount = float(row[-1].replace('$', '').strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return total_amount, date_str, line_items

def calculate_totals_and_items(directory_path):
    """ Calculate the grand total of all totals and item-wise subtotals in CSV files within the specified directory. """
    grand_total = 0.0
    totals_by_date = {}
    item_subtotals = {}
    errors = 0

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str, line_items = extract_totals_from_csv(file_path)
            
            if date_str:  # Only process if a date is successfully extracted
                grand_total += total
                if date_str in totals_by_date:
                    totals_by_date[date_str] += total
                else:
                    totals_by_date[date_str] = total

                for item, amount in line_items.items():
                    if item in item_subtotals:
                        item_subtotals[item] += amount
                    else:
                        item_subtotals[item] = amount

                print(f"Processed {filename}: Date = {date_str}, Total = ${total}")
            else:
                errors += 1
                print(f"Skipped {filename} due to missing or invalid date.")

    if errors > 0:
        print(f"Skipped {errors} files due to errors.")

    # Attempt to plot only if there are valid dates
    if totals_by_date:
        # Prepare data for plotting by date
        dates = sorted(totals_by_date.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
        totals = [totals_by_date[date] for date in dates]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, totals, marker='o', linestyle='-', color='b')
        plt.title("Total Spend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Spend ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return grand_total, item_subtotals

def save_to_csv(grand_total, item_totals, output_file):
    """Save the grand total and item totals to a CSV file."""
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing the grand total
        writer.writerow(['Grand Total', f"${grand_total}"])
        # Writing item-wise totals
        writer.writerow(['Item', 'Total'])
        for item, total in item_totals.items():
            writer.writerow([item, f"${total}"])
# Parameters
directory_path = 'receipts'
output_csv_file = 'totals_summary.csv'

# Calculating totals
grand_total, item_totals = calculate_totals_and_items(directory_path)

# Printing results to the console
print("Grand Total:", grand_total)
for item, total in item_totals.items():
    print(f"{item}: ${total}")

# Saving to CSV
save_to_csv(grand_total, item_totals, output_csv_file)