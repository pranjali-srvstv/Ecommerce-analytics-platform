import sqlite3
import pandas as pd
import os

print("🗄️ Creating SQLite database...")

# Connect to SQLite database
conn = sqlite3.connect('data/ecommerce.db')

# Load CSV data
df = pd.read_csv('data/ecommerce_data.csv')

# Create orders table
df.to_sql('orders', conn, if_exists='replace', index=False)

# Test the database
test_query = pd.read_sql_query("SELECT * FROM orders LIMIT 5", conn)
print("✅ Database created successfully!")
print("📋 Sample data from database:")
print(test_query)

# Show table info
table_info = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(f"📊 Tables in database: {list(table_info['name'])}")

conn.close()
print("🎉 Phase 1 completed! Database is ready.")