import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV files
totals_data = pd.read_csv('totals_summary.csv')
items_data = pd.read_csv('items_summary.csv')

# Convert date from string to datetime format for better handling in plots
totals_data['Date'] = pd.to_datetime(totals_data['Date'], errors='coerce')

# Time Series Plot for total sales over time
plt.figure(figsize=(10, 5))
plt.plot(totals_data['Date'], totals_data['Total'].str.replace('$', '').astype(float), marker='o')
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales ($)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Bar Chart for top 10 items by total sales
top_items = items_data.nlargest(10, 'Total Cost')
plt.figure(figsize=(10, 5))
plt.bar(top_items['Item'], top_items['Total Cost'].str.replace('$', '').astype(float))
plt.title('Top 10 Items by Total Sales')
plt.xlabel('Item')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Additional plots can be created similarly
