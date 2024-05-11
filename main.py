import os
import csv
import re
from datetime import datetime


def extract_info_from_csv(file_path):
    items = {}
    total_amount = 0.0
    date_str = ""

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if "Invoice" in row[0]:
                    date_str = datetime.strptime(row[1].split('-')[1].strip(), "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d")
                if row[0].isdigit() and len(row) >= 5:
                    item_description = row[1].strip()
                    price_string = row[-1].replace('$', '').replace(',', '').strip()
                    if price_string:
                        try:
                            price = float(price_string)
                            if item_description in items:
                                item_data = items[item_description]
                                item_data['total'] += price
                                item_data['count'] += 1
                                item_data['min'] = min(item_data['min'], price)
                                item_data['max'] = max(item_data['max'], price)
                            else:
                                items[item_description] = {
                                    'total': price,
                                    'count': 1,
                                    'min': price,
                                    'max': price
                                }
                        except ValueError:
                            print(f"Invalid price format: {price_string}")

                if "Total" in row[0]:
                    total_string = row[-1].replace('$', '').replace(',', '').strip()
                    if total_string:
                        try:
                            total_amount = float(total_string)
                        except ValueError:
                            print(f"Invalid total format: {total_string}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    print(f"Items processed from {file_path}: {items}")  # Debugging statement
    return total_amount, date_str, items

def process_receipts(directory_path):
    grand_total = 0.0
    totals_by_date = {}
    all_items = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str, items = extract_info_from_csv(file_path)
            grand_total += total
            if date_str in totals_by_date:
                totals_by_date[date_str] += total
            else:
                totals_by_date[date_str] = total

            for item, data in items.items():
                if item in all_items:
                    all_items[item]['total'] += data['total']
                    all_items[item]['count'] += data['count']
                    all_items[item]['min'] = min(all_items[item]['min'], data['min'])
                    all_items[item]['max'] = max(all_items[item]['max'], data['max'])
                else:
                    all_items[item] = data

    # Output results
    print(f"Grand Total: ${grand_total:.2f}")
    for date, total in totals_by_date.items():
        print(f"Date: {date}, Total: ${total:.2f}")
    for item, data in sorted(all_items.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"Item: {item}, Total: ${data['total']:.2f}, Count: {data['count']}, Min: ${data['min']:.2f}, Max: ${data['max']:.2f}")

process_receipts('receipts')


def calculate_totals(directory_path):
    grand_total = 0.0
    totals_by_date = {}
    all_items = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str, items = extract_info_from_csv(file_path)
            print(f"File: {filename}, Date: {date_str}, Total: {total}")  # Debugging output
            if date_str:
                grand_total += total
                if date_str in totals_by_date:
                    totals_by_date[date_str] += total
                else:
                    totals_by_date[date_str] = total

                for item, data in items.items():
                    if item in all_items:
                        all_items[item]['total'] += data['total']
                        all_items[item]['count'] += data['count']
                    else:
                        all_items[item] = {'total': data['total'], 'count': 1}

    print(f"Calculated Grand Total: ${grand_total:.2f}")  # Debugging output
    return grand_total, totals_by_date, all_items


def save_to_csv(totals_by_date, items, grand_total, output_file, items_file):
    # Writing date and total information to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Total'])
        for date, total in sorted(totals_by_date.items()):
            writer.writerow([date, f"${total:.2f}"])
        writer.writerow(['Grand Total', f"${grand_total:.2f}"])

    # Writing item details to CSV
    with open(items_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item', 'Total Cost', 'Frequency', 'Min Price', 'Max Price', 'Average Price'])
        for item, data in sorted(items.items(), key=lambda x: x[1]['total'], reverse=True):
            if 'min' in data and 'max' in data:  # Checking that all required fields are present
                average_price = data['total'] / data['count'] if data['count'] > 0 else 0
                writer.writerow([item, f"${data['total']:.2f}", data['count'], f"${data['min']:.2f}", f"${data['max']:.2f}", f"${average_price:.2f}"])
            else:
                print(f"Missing 'min' or 'max' for item {item}: {data}")


# Execution
directory_path = 'receipts'
output_csv_file = 'totals_summary.csv'
items_csv_file = 'items_summary.csv'
grand_total, totals_by_date, all_items = calculate_totals(directory_path)
print(f"Grand Total: ${grand_total:.2f}")
#save_to_csv(totals_by_date, all_items, grand_total, output_csv_file, items_csv_file)
process_receipts(directory_path)