import sqlite3
from pathlib import Path
import pandas as pd


def create_db():

    columnas = ['id', 'inventory_name', 'contact_name', 'stock', 'last_revenue',
                'current_revenue', 'refund', 'company_name', 'categories', 'rating']

    Path('./ng.db').touch()
    conn = sqlite3.connect('./ng.db')
    c = conn.cursor()
    c.execute('''DROP TABLE negotiation''')

    c.execute('''CREATE TABLE negotiation (id int, inventory_name text, contact_name text, stock int, last_revenue float,
                current_revenue float, refund float, company_name text, categories text, rating float)''')

    ng_data = pd.read_csv('./SampleCSVFile_556kb.csv',
                          engine='python', names=columnas)
    ng_data.to_sql('negotiation', conn, if_exists='append', index=False)

if __name__ == '__main__':
    create_db()