import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data, assuming no header is present in the CSV file
df = pd.read_csv('item_list.csv', header=None)

# Assign column names manually if your CSV doesn't have headers
df.columns = ['Item', 'Total', 'Count', 'Min', 'Max']

# Clean and prepare the data
df['Total'] = df['Total'].str.replace('Total: \$', '').str.replace(',', '').astype(float)
df['Min'] = df['Min'].str.replace('Min: \$', '').str.replace(',', '').astype(float)
df['Max'] = df['Max'].str.replace('Max: \$', '').str.replace(',', '').astype(float)
df['Count'] = df['Count'].str.replace('Count: ', '').astype(int)

# Filter out specified rows using a more comprehensive regex pattern and a condition for zero total
exclude_patterns = 'Item: Total|Item: Sub-Total|Item: Tax|MC/VISA 6866|IOU PAYMNT'
df_filtered = df[~df['Item'].str.contains(exclude_patterns, regex=True) & (df['Total'] != 0.00)]

# Sort and export filtered data to CSV
sorted_items = df_filtered.sort_values(by='Total', ascending=False)
sorted_items.to_csv('sorted_item_totals.csv', index=False)

# Visualization and saving plots
# Top items
plt.figure(figsize=(12, 8))
top_plot = sns.barplot(data=sorted_items.head(10), x='Total', y='Item')
plt.title('Top 10 Most Expensive Items Excluding Specified Totals')
plt.xlabel('Total Cost ($)')
plt.ylabel('Item')
plt.tight_layout()
plt.savefig('top_items.png')
plt.show()

# Distribution of item counts
plt.figure(figsize=(12, 8))
count_plot = sns.histplot(sorted_items['Count'], bins=30, kde=True)
plt.title('Distribution of Item Counts for Other Items')
plt.xlabel('Item Count')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('item_counts_distribution.png')
plt.show()

# Scatter plot of Total vs Count
plt.figure(figsize=(12, 8))
scatter_plot = sns.scatterplot(data=sorted_items, x='Count', y='Total')
plt.title('Scatter Plot of Total Cost vs. Item Count for Other Items')
plt.xlabel('Item Count')
plt.ylabel('Total Cost ($)')
plt.tight_layout()
plt.savefig('total_vs_count_scatter.png')
plt.show()
