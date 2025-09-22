import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sqlite3

print("📊 Starting Phase 1: Data Collection & Database Setup...")

# Create data folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate sample data
np.random.seed(42)
num_orders = 2000

# Date range
start_date = datetime(2023, 1, 1)
date_range = [start_date + timedelta(days=x) for x in range(365)]

# Product data
products = [
    ('iPhone 14', 'Electronics', 999.99),
    ('MacBook Pro', 'Electronics', 1299.99),
    ('AirPods', 'Electronics', 179.99),
    ('T-Shirt', 'Clothing', 24.99),
    ('Jeans', 'Clothing', 59.99),
    ('Blender', 'Home & Kitchen', 49.99),
    ('Coffee Maker', 'Home & Kitchen', 89.99),
    ('Python Programming Book', 'Books', 39.99),
    ('Yoga Mat', 'Sports', 29.99),
    ('Face Cream', 'Beauty', 19.99)
]

# Generate orders
data = []
for order_id in range(1, num_orders + 1):
    customer_id = f"CUST_{np.random.randint(1, 101):03d}"
    order_date = np.random.choice(date_range)
    product_name, category, base_price = products[np.random.randint(0, len(products))]
    
    quantity = np.random.randint(1, 4)
    unit_price = round(base_price * np.random.uniform(0.8, 1.2), 2)
    total_amount = round(unit_price * quantity, 2)
    
    data.append({
        'order_id': order_id,
        'customer_id': customer_id,
        'product_name': product_name,
        'category': category,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'unit_price': unit_price,
        'quantity': quantity,
        'total_amount': total_amount
    })

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv('data/ecommerce_data.csv', index=False)
print("✅ Sample data generated and saved to data/ecommerce_data.csv")
print(f"📊 Generated {len(df)} orders")
print(df.head(3))