from flask import Flask
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('data/ecommerce.db')
    metrics = pd.read_sql_query("SELECT COUNT(*) as orders FROM orders", conn)
    conn.close()
    return f"E-commerce Analytics: {metrics.iloc[0]['orders']} orders processed"

if __name__ == '__main__':
    app.run(debug=True)