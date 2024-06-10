import os
import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

def extract_info_from_csv(file_path):
    items = {}
    total_amount = 0.0
    date_str = ""

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:  # Ensure row has at least 2 columns
                    continue
                if "Invoice" in row[0]:
                    try:
                        date_str = datetime.strptime(row[1].split('-')[1].strip(), "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d")
                    except Exception as e:
                        print(f"Error parsing date from row {row}: {e}")
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

                if len(row) >= 2 and "Total" in row[1]:  # Ensure row has at least 2 columns and "Total" in second column
                    total_string = row[-1].replace('$', '').replace(',', '').strip()
                    if total_string:
                        try:
                            total_amount = float(total_string)
                        except ValueError:
                            print(f"Invalid total format: {total_string}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    print(f"Items processed from {file_path}: {items}")  # Debugging statement
    print(f"Total from {file_path}: {total_amount}")  # Debugging statement
    return total_amount, date_str, items


def process_receipts(directory_path):
    grand_total = 0.0
    totals_by_date = {}
    totals_by_month = defaultdict(float)
    monthly_counts = defaultdict(int)
    all_items = {}
    processed_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str, items = extract_info_from_csv(file_path)
            grand_total += total
            if date_str in totals_by_date:
                totals_by_date[date_str] += total
            else:
                totals_by_date[date_str] = total

            month_str = date_str[:7]  # Extract the year-month part of the date
            totals_by_month[month_str] += total
            monthly_counts[month_str] += 1

            for item, data in items.items():
                if item in all_items:
                    all_items[item]['total'] += data['total']
                    all_items[item]['count'] += data['count']
                    all_items[item]['min'] = min(all_items[item]['min'], data['min'])
                    all_items[item]['max'] = max(all_items[item]['max'], data['max'])
                else:
                    all_items[item] = data

            # Collect data for processed file
            processed_data.append((date_str, items))

    monthly_averages = {month: totals_by_month[month] / monthly_counts[month] for month in totals_by_month}

    # Output results
    print(f"Grand Total: ${grand_total:.2f}")
    for date, total in totals_by_date.items():
        print(f"Date: {date}, Total: ${total:.2f}")
    for month, avg in monthly_averages.items():
        print(f"Month: {month}, Average Total: ${avg:.2f}")
    for item, data in sorted(all_items.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"Item: {item}, Total: ${data['total']:.2f}, Count: {data['count']}, Min: ${data['min']:.2f}, Max: ${data['max']:.2f}")

    return processed_data, grand_total, totals_by_date, all_items, monthly_averages


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


def save_to_csv(totals_by_date, items, grand_total, output_file, items_file, processed_file, monthly_averages):
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

    # Writing processed data details to CSV
    with open(processed_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Item', 'Total Cost', 'Frequency', 'Min Price', 'Max Price'])
        for date, items in processed_data:
            for item, data in items.items():
                writer.writerow([date, item, f"${data['total']:.2f}", data['count'], f"${data['min']:.2f}", f"${data['max']:.2f}"])

    # Writing monthly averages to CSV
    with open(os.path.join(output_dir, 'monthly_averages.csv'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Month', 'Average Total'])
        for month, avg in sorted(monthly_averages.items()):
            writer.writerow([month, f"${avg:.2f}"])


def save_most_bought_items_to_csv(items, output_csv_file):
    # Sorting items by count in descending order
    sorted_items = sorted(items.items(), key=lambda x: x[1]['count'], reverse=True)

    # Writing most bought items and their costs to a CSV file
    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item', 'Count', 'Total Cost'])
        for item, data in sorted_items:
            writer.writerow([item, data['count'], f"${data['total']:.2f}"])


def create_visualizations(output_dir, totals_by_date, items, monthly_averages):
    # Create directory for visualizations
    visualization_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(visualization_dir, exist_ok=True)

    # Visualization 1: Totals by Date
    dates = list(totals_by_date.keys())
    totals = list(totals_by_date.values())

    plt.figure(figsize=(10, 6))
    plt.bar(dates, totals)
    plt.xlabel('Date')
    plt.ylabel('Total Amount')
    plt.title('Total Amount by Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_dir, 'totals_by_date.png'))
    plt.close()

    # Visualization 2: Monthly Averages
    months = list(monthly_averages.keys())
    averages = list(monthly_averages.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, averages)
    plt.xlabel('Month')
    plt.ylabel('Average Total')
    plt.title('Average Total by Month')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_dir, 'monthly_averages.png'))
    plt.close()

    # Visualization 3: Most Bought Items
    item_names = list(items.keys())
    item_totals = [data['total'] for data in items.values()]

    plt.figure(figsize=(10, 6))
    plt.barh(item_names, item_totals)
    plt.xlabel('Total Amount')
    plt.ylabel('Item')
    plt.title('Total Amount by Item')
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_dir, 'items_totals.png'))
    plt.close()

    # Visualization 4: Top 10 Most Bought Items
    exclude_items = {"subtotal", "tax", "total", "balance", "iou", "payment", "debit"}
    filtered_items = {k: v for k, v in items.items() if all(x not in k.lower() for x in exclude_items)}

    sorted_items = sorted(filtered_items.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
    top_items = [item[0] for item in sorted_items]
    top_counts = [item[1]['count'] for item in sorted_items]
    top_totals = [item[1]['total'] for item in sorted_items]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Item')
    ax1.set_ylabel('Count', color=color)
    ax1.bar(top_items, top_counts, color=color, alpha=0.6, label='Count')
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Total Cost', color=color)  # we already handled the x-label with ax1
    ax2.plot(top_items, top_totals, color=color, marker='o', linestyle='-', linewidth=2, label='Total Cost')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Top 10 Most Bought Items')
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(visualization_dir, 'top_10_most_bought_items.png'))
    plt.close()


# Execution
directory_path = 'receipts'
current_date = datetime.now().strftime("%Y-%m-%d")
output_dir = f'output_{current_date}'
os.makedirs(output_dir, exist_ok=True)

output_csv_file = os.path.join(output_dir, 'totals_summary.csv')
items_csv_file = os.path.join(output_dir, 'items_summary.csv')
processed_csv_file = os.path.join(output_dir, 'processed_summary.csv')
most_bought_items_csv_file = os.path.join(output_dir, 'most_bought_items.csv')

processed_data, grand_total, totals_by_date, all_items, monthly_averages = process_receipts(directory_path)
print(f"Grand Total: ${grand_total:.2f}")
save_to_csv(totals_by_date, all_items, grand_total, output_csv_file, items_csv_file, processed_csv_file, monthly_averages)
save_most_bought_items_to_csv(all_items, most_bought_items_csv_file)

# Create visualizations
create_visualizations(output_dir, totals_by_date, all_items, monthly_averages)
