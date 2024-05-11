# import os
# import csv
# from datetime import datetime
# import matplotlib.pyplot as plt

# def extract_totals_from_csv(file_path):
#     total_amount = 0.0
#     date_str = ""
#     line_items = {}
#     try:
#         with open(file_path, mode='r', newline='') as file:
#             reader = csv.reader(file)
#             processing_items = False
#             for row in reader:
#                 if not row:
#                     continue
#                 if "Invoice" in row[0] and '-' in row[0]:
#                     try:
#                         date_part = row[0].split('-')[1].strip()
#                         date_str = datetime.strptime(date_part, "%m/%d/%Y %H:%M %p").strftime("%Y-%m-%d")
#                     except ValueError:
#                         print(f"Date format error in {file_path}")
#                         continue
#                 elif "UPC" in row[0] and "Price" in row[-1]:
#                     processing_items = True
#                 elif processing_items and len(row) >= 3 and row[0].isdigit():
#                     try:
#                         price = float(row[-1].replace('$', '').strip())
#                         description = row[1].strip()
#                         line_items[description] = line_items.get(description, 0) + price
#                     except ValueError:
#                         print(f"Price format error in {file_path} for row: {row}")
#                 elif "Total" in row[0] and row[-1].startswith('$'):
#                     try:
#                         total_amount = float(row[-1].replace('$', '').strip())
#                     except ValueError:
#                         print(f"Total format error in {file_path}")
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")
#     return total_amount, date_str, line_items

# def plot_and_save(data, title, x_label, y_label, filename):
#     if data:
#         dates, totals = zip(*sorted(data.items()))
#         plt.figure(figsize=(10, 5))
#         plt.plot(dates, totals, marker='o', linestyle='-', color='b')
#         plt.title(title)
#         plt.xlabel(x_label)
#         plt.ylabel(y_label)
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.savefig(filename)
#         plt.close()
#     else:
#         print(f"No data to plot for {title}")


# def calculate_totals_and_items(directory_path):
#     grand_total = 0.0
#     totals_by_date = {}
#     item_subtotals = {}

#     for filename in os.listdir(directory_path):
#         if filename.endswith('.csv'):
#             file_path = os.path.join(directory_path, filename)
#             total, date_str, line_items = extract_totals_from_csv(file_path)
#             if date_str:
#                 grand_total += total
#                 totals_by_date[date_str] = totals_by_date.get(date_str, 0) + total
#                 for item, amount in line_items.items():
#                     item_subtotals[item] = item_subtotals.get(item, 0) + amount
#                 print(f"Processed {filename}: Date = {date_str}, Total = ${total:.2f}")
    
#     plot_and_save(totals_by_date, "Total Spend Over Time", "Date", "Total Spend ($)", "total_spend_over_time.png")
#     if item_subtotals:
#         plot_and_save(item_subtotals, "Subtotals by Item", "Item", "Subtotal ($)", "subtotals_by_item.png")
    
#     return grand_total, item_subtotals

# # Example usage:
# directory_path = 'receipts'
# grand_total, item_subtotals = calculate_totals_and_items(directory_path)
# print("Grand Total:", grand_total)
# for item, total in sorted(item_subtotals.items()):
#     print(f"{item}: ${total:.2f}")
