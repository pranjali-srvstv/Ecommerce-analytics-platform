# export_static.py - Simple static dashboard creator
import sqlite3
import pandas as pd

def create_static_dashboard():
    print('Creating static dashboard...')
    
    # Get data
    conn = sqlite3.connect('data/ecommerce.db')
    metrics = pd.read_sql_query('SELECT COUNT(*) as orders, SUM(total_amount) as revenue FROM orders', conn)
    conn.close()
    
    # Simple HTML
    html = '''<html>
<head><title>Dashboard</title>
<style>
body { background: #0f172a; color: white; font-family: Arial; padding: 20px; }
.card { background: #1e293b; padding: 20px; margin: 10px; border-radius: 10px; }
</style>
</head>
<body>
<h1>E-commerce Analytics</h1>
<div class="card">
    <h3>Total Revenue: ${REVENUE}</h3>
    <h3>Total Orders: {ORDERS}</h3>
</div>
<p>Portfolio Project - Data Analytics</p>
</body>
</html>'''
    
    html = html.replace('{REVENUE}', f'{metrics.iloc[0]["revenue"]:,.2f}')
    html = html.replace('{ORDERS}', str(metrics.iloc[0]["orders"]))
    
    with open('dashboard.html', 'w') as f:
        f.write(html)
    
    print('✅ Dashboard created: dashboard.html')

create_static_dashboard()
