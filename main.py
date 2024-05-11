import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def extract_total_and_date_from_csv(file_path):
    """ Extract the total and date from the CSV file. """
    total_amount = 0.0
    date_str = ""
    try:
        with open(file_path, mode='r', newline='') as file:
            lines = file.readlines()
            # Extract date from the 5th line
            date_line = lines[4]
            date_str = date_line.split('-')[1].strip()[:10]  # Extract the date part only
            # Read the last few lines where the total should be
            for line in reversed(lines[-5:]):
                if "Total" in line:
                    total_amount = float(line.split(',')[-1].replace('"', '').replace('$', '').strip())
                    break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return total_amount, date_str

def calculate_grand_total(directory_path):
    """ Calculate the grand total of all totals in CSV files within the specified directory and plot them. """
    totals_by_date = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            total, date_str = extract_total_and_date_from_csv(file_path)
            if date_str in totals_by_date:
                totals_by_date[date_str] += total
            else:
                totals_by_date[date_str] = total
            print(f"Processed {filename}: Date = {date_str}, Total = ${total}")

    # Prepare data for plotting
    dates = sorted(totals_by_date.keys(), key=lambda x: datetime.strptime(x, "%m/%d/%Y"))
    totals = [totals_by_date[date] for date in dates]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(dates, totals, marker='o', linestyle='-', color='b')
    plt.title("Total Spend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Spend ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return sum(totals)

# Example usage (uncomment in a live Python environment):
directory_path = 'receipts'
print("Grand Total:", calculate_grand_total(directory_path))

