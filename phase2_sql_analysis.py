import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

print("📊 Starting Phase 2: SQL Business Analysis...")

# Connect to database
conn = sqlite3.connect('data/ecommerce.db')

print("✅ Connected to database")

# 1. BASIC BUSINESS METRICS
print("\n" + "="*50)
print("1. BASIC BUSINESS METRICS")
print("="*50)

# Total revenue and orders
basic_metrics = pd.read_sql_query("""
    SELECT 
        COUNT(*) as total_orders,
        SUM(total_amount) as total_revenue,
        AVG(total_amount) as avg_order_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM orders
""", conn)

print("📈 Business Overview:")
print(f"   Total Orders: {basic_metrics.iloc[0]['total_orders']}")
print(f"   Total Revenue: ${basic_metrics.iloc[0]['total_revenue']:,.2f}")
print(f"   Average Order Value: ${basic_metrics.iloc[0]['avg_order_value']:.2f}")
print(f"   Unique Customers: {basic_metrics.iloc[0]['unique_customers']}")

# 2. MONTHLY SALES TREND
print("\n" + "="*50)
print("2. MONTHLY SALES TREND")
print("="*50)

monthly_sales = pd.read_sql_query("""
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(total_amount) as monthly_revenue,
        COUNT(*) as order_count
    FROM orders
    GROUP BY month
    ORDER BY month
""", conn)

print("📅 Monthly Performance:")
for _, row in monthly_sales.iterrows():
    print(f"   {row['month']}: ${row['monthly_revenue']:,.2f} ({row['order_count']} orders)")

# 3. CATEGORY PERFORMANCE
print("\n" + "="*50)
print("3. CATEGORY PERFORMANCE")
print("="*50)

category_performance = pd.read_sql_query("""
    SELECT 
        category,
        SUM(total_amount) as revenue,
        COUNT(*) as order_count,
        AVG(total_amount) as avg_order_value
    FROM orders
    GROUP BY category
    ORDER BY revenue DESC
""", conn)

print("🏷️ Category Analysis:")
for _, row in category_performance.iterrows():
    print(f"   {row['category']:15} ${row['revenue']:>10,.2f} ({row['order_count']:>3} orders)")

# 4. CUSTOMER SEGMENTATION (RFM Analysis)
print("\n" + "="*50)
print("4. CUSTOMER SEGMENTATION (RFM ANALYSIS)")
print("="*50)

rfm_analysis = pd.read_sql_query("""
    WITH customer_stats AS (
        SELECT 
            customer_id,
            COUNT(*) as frequency,
            SUM(total_amount) as monetary,
            MAX(order_date) as last_order_date,
            JULIANDAY('2023-12-31') - JULIANDAY(MAX(order_date)) as recency_days
        FROM orders
        GROUP BY customer_id
    )
    SELECT 
        customer_id,
        frequency,
        monetary,
        recency_days,
        CASE 
            WHEN recency_days <= 30 THEN 'High'
            WHEN recency_days <= 90 THEN 'Medium'
            ELSE 'Low'
        END as recency_score,
        CASE 
            WHEN frequency > 30 THEN 'High'
            WHEN frequency > 15 THEN 'Medium'
            ELSE 'Low'
        END as frequency_score,
        CASE 
            WHEN monetary > 5000 THEN 'High'
            WHEN monetary > 2000 THEN 'Medium'
            ELSE 'Low'
        END as monetary_score
    FROM customer_stats
    ORDER BY monetary DESC
    LIMIT 10
""", conn)

print("👥 Top 10 Customers by Spending:")
for _, row in rfm_analysis.iterrows():
    print(f"   {row['customer_id']}: ${row['monetary']:,.2f} ({row['frequency']} orders)")

# 5. PRODUCT PERFORMANCE
print("\n" + "="*50)
print("5. PRODUCT PERFORMANCE")
print("="*50)

product_performance = pd.read_sql_query("""
    SELECT 
        product_name,
        category,
        SUM(total_amount) as revenue,
        SUM(quantity) as total_quantity,
        COUNT(*) as order_count
    FROM orders
    GROUP BY product_name, category
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

print("📦 Top 10 Products:")
for _, row in product_performance.iterrows():
    print(f"   {row['product_name']:25} ${row['revenue']:>10,.2f} ({row['total_quantity']} units)")

# 6. SALES TREND ANALYSIS
print("\n" + "="*50)
print("6. SALES TREND ANALYSIS")
print("="*50)

weekly_trend = pd.read_sql_query("""
    SELECT 
        strftime('%Y-%W', order_date) as week,
        SUM(total_amount) as weekly_revenue,
        COUNT(*) as weekly_orders
    FROM orders
    GROUP BY week
    ORDER BY week
    LIMIT 10
""", conn)

print("📊 Recent Weekly Trends:")
for _, row in weekly_trend.iterrows():
    print(f"   Week {row['week']}: ${row['weekly_revenue']:,.2f}")

# Save analysis results to CSV
basic_metrics.to_csv('data/business_metrics.csv', index=False)
monthly_sales.to_csv('data/monthly_sales.csv', index=False)
category_performance.to_csv('data/category_performance.csv', index=False)

print("\n✅ Analysis completed!")
print("💾 Results saved to CSV files in data/ folder")

conn.close()

print("\n🎉 Phase 2 completed! Ready for Phase 3 (Visualization)")