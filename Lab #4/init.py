import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("company_data.db")
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS Orders""")
cur.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    product TEXT,
    quantity INTEGER,
    price_per_unit REAL,
    order_date TEXT,
    status TEXT
)
""")

customers = [f"Customer_{i}" for i in range(1, 21)]
products = ["Laptop", "Phone", "Tablet", "Headphones", "Monitor", "Mouse", "Keyboard"]
statuses = ["Completed", "Pending", "Cancelled"]

orders = []
for _ in range(120):
    customer = random.choice(customers)
    product = random.choice(products)
    quantity = random.randint(1, 5)
    price = round(random.uniform(50, 1500), 2)
    days_ago = random.randint(0, 60)
    order_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    status = random.choice(statuses)
    orders.append((customer, product, quantity, price, order_date, status))

cur.executemany("""
INSERT INTO Orders (customer_name, product, quantity, price_per_unit, order_date, status)
VALUES (?, ?, ?, ?, ?, ?)
""", orders)

conn.commit()
conn.close()