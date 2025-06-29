import pandas as pd
import os
from django.core.cache import cache

# Load the data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'retail.xlsx')
df = pd.read_excel(file_path, sheet_name='retail', engine='openpyxl', usecols=['CustomerID', 'Description', 'InvoiceNo'])
print(df.columns)

# Drop missing values
df.dropna(subset=['CustomerID', 'Description'], inplace=True)

# Grouping for easier access later
grouped = df.groupby('CustomerID')

# 🔮 Main function
def recommend_product_full(customer_id):
    customer_id = float(customer_id)

    if customer_id not in grouped.groups:
        return None, [], []

    customer_data = grouped.get_group(customer_id)
    top_product = customer_data['Description'].value_counts().idxmax()

    # ✅ Similar products (same Invoice or frequency)
    similar_products = df[df['Description'] == top_product]['InvoiceNo'].unique()
    similar_df = df[df['InvoiceNo'].isin(similar_products)]
    similar_items = similar_df['Description'].unique().tolist()

    # ✅ People who bought this also bought
    also_bought_df = df[df['InvoiceNo'].isin(similar_products)]
    also_bought_all = also_bought_df['Description'].unique().tolist()
    also_bought_unique = list(set(also_bought_all) - {top_product})

    return top_product, similar_items[:5], also_bought_unique[:5]

