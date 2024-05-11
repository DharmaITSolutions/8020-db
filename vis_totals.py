import matplotlib.pyplot as plt
import csv

def plot_totals_from_csv(csv_file):
    """Plot item totals from a CSV file."""
    items = []
    totals = []

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line for "Grand Total"
        next(reader)  # Skip the grand total line
        next(reader)  # Skip the header line for items

        for row in reader:
            if row:  # Ensure the row is not empty
                items.append(row[0])  # The item name
                total_value = float(row[1].replace('$', '').strip())  # Convert the total to float
                totals.append(total_value)

    # Create a bar plot
    plt.figure(figsize=(14, 7))
    plt.bar(items, totals, color='blue')
    plt.xlabel('Items')
    plt.ylabel('Total ($)')
    plt.title('Total Sales by Item')
    plt.xticks(rotation=90)  # Rotate item names for better visibility
    plt.tight_layout()
    plt.show()

# Example call to the function
plot_totals_from_csv('totals_summary.csv')
