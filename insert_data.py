import sqlite3
import yfinance as yf
from datetime import datetime, timedelta

def connect():
    conn = sqlite3.connect('stock_analysis.db')
    return conn, conn.cursor()

def get_stock_names():
    with open('stock_names.txt', 'r') as file:
        stock_names = sorted(file.read().splitlines())
    return stock_names

def get_start_and_end_dates():
    start_date = datetime.now().date() - timedelta(days=8)
    end_date = datetime.now().date()
    return start_date, end_date

def insert_historical_data(cursor):
    stock_names = get_stock_names()
    start_date, end_date = get_start_and_end_dates()
    for name in stock_names:
        cursor.execute('INSERT INTO scripts(name) VALUES (?)', (name,))
        data = yf.download(name + '.NS', start=start_date, end=end_date, interval='30m')
        data['time'] = [index.time().strftime('%H:%M') for index, row in data.iterrows()]
        data['Cumulative Volume'] = data['Volume'].cumsum()
        df = data.groupby('time')['Cumulative Volume'].mean().round()
        for index, row in df.items():
            cursor.execute(f'''
                        INSERT INTO historical_data_avg
                        VALUES (?, ?, ?)
                    ''', (index, name, int(row)))
        

def get_data():
    conn, cursor = connect()
    insert_historical_data(cursor)
    conn.commit()
    conn.close()
