# export_beautiful.py - Preserves your dark theme design
import sqlite3
import pandas as pd

def export_beautiful_dashboard():
    print("🔄 Creating beautiful static version...")
    
    # Get your real data
    conn = sqlite3.connect('data/ecommerce.db')
    metrics = pd.read_sql_query("""
        SELECT COUNT(*) as total_orders, SUM(total_amount) as total_revenue,
               AVG(total_amount) as avg_order_value, 
               COUNT(DISTINCT customer_id) as unique_customers
        FROM orders
    """, conn)
    conn.close()
    
    # Read your original beautiful HTML
    with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
        beautiful_html = f.read()
    
    # Replace placeholder data with real data
    beautiful_html = beautiful_html.replace('$245,000', f'${metrics.iloc[0]["total_revenue"]:,.2f}')
    beautiful_html = beautiful_html.replace('1,200', f'{metrics.iloc[0]["total_orders"]:,}')
    beautiful_html = beautiful_html.replace('$204', f'${metrics.iloc[0]["avg_order_value"]:.2f}')
    beautiful_html = beautiful_html.replace('100', f'{metrics.iloc[0]["unique_customers"]:,}')
    
    # Remove the Flask script tag to make it truly static
    beautiful_html = beautiful_html.replace(
        '<script src="{{ url_for(\'static\', filename=\'js/script.js\') }}"></script>',
        '<!-- Static version - original design preserved -->'
    )
    
    # Save as beautiful static version
    with open('beautiful_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(beautiful_html)
    
    print("✅ Beautiful static dashboard created: beautiful_dashboard.html")
    print("🎨 Your original design is preserved with real data!")

if __name__ == "__main__":
    export_beautiful_dashboard()