from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for main metrics"""
    conn = sqlite3.connect('data/ecommerce.db')
    
    # Get basic metrics
    metrics = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM orders
    """, conn)
    
    # Calculate growth percentages (mock data for now)
    revenue_growth = 12.5
    orders_growth = 8.2
    conversion_growth = -2.1
    aov_growth = 5.3
    
    conn.close()
    
    return jsonify({
        'total_revenue': round(float(metrics.iloc[0]['total_revenue']), 2),
        'total_orders': int(metrics.iloc[0]['total_orders']),
        'avg_order_value': round(float(metrics.iloc[0]['avg_order_value']), 2),
        'unique_customers': int(metrics.iloc[0]['unique_customers']),
        'growth_rates': {
            'revenue': revenue_growth,
            'orders': orders_growth,
            'conversion': conversion_growth,
            'aov': aov_growth
        }
    })

@app.route('/api/monthly-data')
def get_monthly_data():
    """API endpoint for monthly revenue data"""
    conn = sqlite3.connect('data/ecommerce.db')
    
    monthly_data = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', order_date) as month,
            SUM(total_amount) as revenue,
            COUNT(*) as orders
        FROM orders
        GROUP BY month
        ORDER BY month
    """, conn)
    
    conn.close()
    
    return jsonify(monthly_data.to_dict('records'))

@app.route('/api/categories')
def get_categories():
    """API endpoint for category data"""
    conn = sqlite3.connect('data/ecommerce.db')
    
    categories = pd.read_sql_query("""
        SELECT 
            category,
            COUNT(*) as order_count,
            SUM(total_amount) as revenue
        FROM orders
        GROUP BY category
        ORDER BY revenue DESC
    """, conn)
    
    conn.close()
    
    return jsonify(categories.to_dict('records'))

@app.route('/api/recent-orders')
def get_recent_orders():
    """API endpoint for recent orders table"""
    conn = sqlite3.connect('data/ecommerce.db')
    
    orders = pd.read_sql_query("""
        SELECT 
            order_id,
            customer_id,
            order_date,
            total_amount,
            product_name
        FROM orders
        ORDER BY order_date DESC
        LIMIT 10
    """, conn)
    
    conn.close()
    
    return jsonify(orders.to_dict('records'))

if __name__ == '__main__':
    print("🚀 Starting E-commerce Dashboard...")
    print("📊 Access your dashboard at: http://localhost:5000")
    print("📈 API endpoints available:")
    print("   - http://localhost:5000/api/metrics")
    print("   - http://localhost:5000/api/monthly-data")
    print("   - http://localhost:5000/api/categories")
    app.run(debug=True, host='0.0.0.0', port=5000)