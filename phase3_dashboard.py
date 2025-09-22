import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set up professional styling
plt.style.use('seaborn-v0_8')
print("📊 Starting Phase 3: Data Visualization Dashboard...")

# Connect to database
conn = sqlite3.connect('data/ecommerce.db')

# 1. Load data for visualization
monthly_sales = pd.read_sql_query("""
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(total_amount) as monthly_revenue,
        COUNT(*) as order_count
    FROM orders
    GROUP BY month
    ORDER BY month
""", conn)

category_data = pd.read_sql_query("""
    SELECT 
        category,
        SUM(total_amount) as revenue,
        COUNT(*) as order_count
    FROM orders
    GROUP BY category
    ORDER BY revenue DESC
""", conn)

customer_data = pd.read_sql_query("""
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 15
""", conn)

product_data = pd.read_sql_query("""
    SELECT 
        product_name,
        SUM(total_amount) as revenue,
        SUM(quantity) as units_sold
    FROM orders
    GROUP BY product_name
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

# 2. Create Professional Dashboard
fig = plt.figure(figsize=(20, 15))
fig.suptitle('E-commerce Business Intelligence Dashboard', fontsize=20, fontweight='bold')

# Plot 1: Monthly Revenue Trend
ax1 = plt.subplot(2, 3, 1)
plt.plot(monthly_sales['month'], monthly_sales['monthly_revenue'], 
         marker='o', linewidth=2, markersize=6, color='#2E86AB')
plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels on points
for i, (month, revenue) in enumerate(zip(monthly_sales['month'], monthly_sales['monthly_revenue'])):
    if i % 2 == 0:  # Show every other label to avoid clutter
        plt.annotate(f'${revenue:,.0f}', (month, revenue), 
                    textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# Plot 2: Category Performance (Pie Chart)
ax2 = plt.subplot(2, 3, 2)
colors = plt.cm.Set3(np.linspace(0, 1, len(category_data)))
wedges, texts, autotexts = plt.pie(category_data['revenue'], 
                                   labels=category_data['category'], 
                                   autopct='%1.1f%%',
                                   colors=colors,
                                   startangle=90)
plt.title('Revenue by Category', fontsize=14, fontweight='bold')

# Make percentages bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# Plot 3: Top Customers Bar Chart
ax3 = plt.subplot(2, 3, 3)
bars = plt.barh(customer_data['customer_id'], customer_data['total_spent'], 
                color='#A23B72', alpha=0.7)
plt.title('Top 15 Customers by Spending', fontsize=14, fontweight='bold')
plt.xlabel('Total Spent ($)')

# Add value labels on bars
for bar, value in zip(bars, customer_data['total_spent']):
    plt.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2, 
             f'${value:,.0f}', ha='left', va='center', fontsize=9)

# Plot 4: Product Performance
ax4 = plt.subplot(2, 3, 4)
y_pos = np.arange(len(product_data['product_name']))
bars = plt.barh(y_pos, product_data['revenue'], color='#F18F01', alpha=0.7)
plt.title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Revenue ($)')
plt.yticks(y_pos, product_data['product_name'])

# Add value labels
for i, (bar, value) in enumerate(zip(bars, product_data['revenue'])):
    plt.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2, 
             f'${value:,.0f}', ha='left', va='center', fontsize=9)

# Plot 5: Orders by Month
ax5 = plt.subplot(2, 3, 5)
bars = plt.bar(monthly_sales['month'], monthly_sales['order_count'], 
               color='#C73E1D', alpha=0.7)
plt.title('Monthly Order Volume', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)

# Add value labels on bars
for bar, value in zip(bars, monthly_sales['order_count']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{value}', ha='center', va='bottom', fontsize=9)

# Plot 6: Summary Statistics
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')  # Turn off axes for text display

# Calculate key metrics
total_revenue = monthly_sales['monthly_revenue'].sum()
total_orders = monthly_sales['order_count'].sum()
avg_order_value = total_revenue / total_orders
best_month = monthly_sales.loc[monthly_sales['monthly_revenue'].idxmax()]
best_category = category_data.iloc[0]

summary_text = f"""
📊 BUSINESS SUMMARY

Total Revenue: ${total_revenue:,.2f}
Total Orders: {total_orders:,}
Avg Order Value: ${avg_order_value:.2f}

🏆 Best Performing:
Month: {best_month['month']}
Revenue: ${best_month['monthly_revenue']:,.2f}

Category: {best_category['category']}
Revenue: ${best_category['revenue']:,.2f}

📈 Key Insights:
- {len(category_data)} product categories
- {len(customer_data)} active customers
- {monthly_sales['month'].nunique()} months of data
"""

plt.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=12, 
         verticalalignment='top', fontfamily='monospace', linespacing=1.5)

plt.tight_layout()
plt.subplots_adjust(top=0.93)

# Save the dashboard
plt.savefig('data/ecommerce_dashboard.png', dpi=300, bbox_inches='tight')
plt.savefig('data/ecommerce_dashboard.pdf', bbox_inches='tight')

print("✅ Dashboard created successfully!")
print("💾 Saved as: data/ecommerce_dashboard.png and .pdf")

# 3. Create Additional Insights
print("\n" + "="*50)
print("ADDITIONAL BUSINESS INSIGHTS")
print("="*50)

# Customer segmentation analysis
customer_segments = pd.read_sql_query("""
    WITH customer_stats AS (
        SELECT 
            customer_id,
            COUNT(*) as frequency,
            SUM(total_amount) as monetary,
            JULIANDAY('2023-12-31') - JULIANDAY(MAX(order_date)) as recency_days
        FROM orders
        GROUP BY customer_id
    )
    SELECT 
        CASE 
            WHEN monetary > 5000 THEN 'VIP'
            WHEN monetary > 2000 THEN 'Loyal'
            WHEN monetary > 500 THEN 'Regular'
            ELSE 'Occasional'
        END as segment,
        COUNT(*) as customer_count,
        AVG(monetary) as avg_spend,
        AVG(frequency) as avg_orders
    FROM customer_stats
    GROUP BY segment
    ORDER BY avg_spend DESC
""", conn)

print("👥 Customer Segmentation Analysis:")
for _, row in customer_segments.iterrows():
    print(f"   {row['segment']:10} - {row['customer_count']:>3} customers, "
          f"Avg Spend: ${row['avg_spend']:,.0f}")

# Monthly growth calculation
monthly_sales['growth'] = monthly_sales['monthly_revenue'].pct_change() * 100
avg_growth = monthly_sales['growth'].mean()

print(f"\n📈 Average Monthly Growth Rate: {avg_growth:.1f}%")

conn.close()

print("\n🎉 Phase 3 completed! You now have a professional dashboard!")
print("\n📁 Your project now includes:")
print("   - data/ecommerce_dashboard.png (Visual dashboard)")
print("   - data/ecommerce_dashboard.pdf (High-quality version)")
print("   - Multiple business insights and analyses")