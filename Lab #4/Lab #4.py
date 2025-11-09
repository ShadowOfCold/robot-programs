import sqlite3
from datetime import datetime, timedelta
import pandas as pd

conn = sqlite3.connect("company_data.db")
df = pd.read_sql("SELECT * FROM Orders", conn)
df['order_date'] = pd.to_datetime(df['order_date'])

date_limit = datetime.now() - timedelta(days=30)
recent_orders = df[(df['order_date'] >= date_limit) & (df['status'] == "Completed")].copy()
recent_orders['total_sales'] = recent_orders['quantity'] * recent_orders['price_per_unit']

agg = (recent_orders.groupby('customer_name')['total_sales'].sum().reset_index().sort_values(by='total_sales', ascending=False).head(5))

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS top_customers (
    customer_name TEXT,
    total_sales REAL
)
""")

cur.execute("DELETE FROM top_customers")
agg.to_sql('top_customers', conn, if_exists='append', index=False)
conn.commit()

top = pd.read_sql("SELECT * FROM top_customers", conn)
print(top)

conn.close()