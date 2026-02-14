import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Load Data
sales = pd.read_csv('data/sales_data.csv')
churn = pd.read_csv('data/customer_churn.csv')

# 2. Data Preparation & Merging
# Normalizing IDs to match (CUST001 -> C00001)
sales['CustomerID'] = sales['Customer_ID'].str.replace('CUST', 'C')
merged_df = pd.merge(sales, churn, on='CustomerID', how='left')

# Datetime Extractions
merged_df['Date'] = pd.to_datetime(merged_df['Date'])
merged_df['Month'] = merged_df['Date'].dt.strftime('%Y-%m')

# 3. Advanced Analysis (Aggregations & Pivot)
# Agg 1: Monthly Totals
monthly_sales = merged_df.groupby('Month')['Total_Sales'].sum()

# Agg 2: Top Customers
top_customers = merged_df.groupby('CustomerID')['Total_Sales'].sum().nlargest(5)

# Pivot Table: Regional Product Performance
pivot_table = merged_df.pivot_table(index='Product', columns='Region', values='Total_Sales', aggfunc='sum')

# 4. Visualizations
if not os.path.exists('visualizations'): os.makedirs('visualizations')

# Chart 1: Trend Line
plt.figure(figsize=(10,5))
monthly_sales.plot(kind='line', marker='o', color='navy')
plt.title('Monthly Sales Performance')
plt.savefig('visualizations/monthly_trend.png')

# Chart 2: Product Heatmap (Pivot visualization)
plt.figure(figsize=(10,6))
sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='YlGnBu')
plt.title('Product Revenue by Region')
plt.savefig('visualizations/product_region_heatmap.png')

print("Task 5 Analysis Complete!")