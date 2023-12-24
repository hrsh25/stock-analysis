import sqlite3
import warnings
import yfinance as yf
from datetime import datetime, timedelta

def connect():
    conn = sqlite3.connect('stock_analysis.db')
    return conn, conn.cursor()

def get_stock_names():
    with open('stock_names.txt', 'r') as file:
        stock_names = file.read().splitlines()
    return stock_names

def get_start_and_end_dates():
    start_date = datetime.now().date() - timedelta(days=58)
    end_date = datetime.now().date()
    return start_date, end_date

def insert_historical_data(cursor, days):
    stock_names = get_stock_names()
    start_date, end_date = get_start_and_end_dates()
    for name in stock_names:
        cursor.execute('INSERT INTO scripts(name) VALUES (?)', (name,))
        data = yf.download(name + '.NS', start=start_date, end=end_date, interval='30m')
        for day in days:
            day_data = data[data.index.weekday == day]
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                day_data['cumulative_volume'] = day_data.groupby(day_data.index.date)['Volume'].cumsum()

            table_name = days[day]
            for index, row in day_data.iterrows():
                date = index.date().strftime('%Y-%m-%d')
                time = index.time().strftime('%H:%M')
                cumulative_volume = row['cumulative_volume']
                cursor.execute(f'''
                    INSERT INTO {table_name}
                    VALUES (?, ?, ?, ?)
                ''', (date, time, name, cumulative_volume))

def insert_average_data(cursor, days, times):
    for day in days.values():
        table_name = '{}_avg'.format(day)
        for time in times:
            cursor.execute(f'''
            INSERT INTO '{table_name}' (script, time, avg_volume)
            SELECT script, '{time}' AS time, AVG(volume) AS avg_volume
            FROM
                '{day}'
            WHERE
                time = '{time}'
            GROUP BY
                script
            ''')

def get_data():
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
    times = ['09:30', '10:00', '10:30', '11:00', '11:30', '12:00', 
            '12:30', '13:00', '13:30', '14:00', '14:30', '15:00']

    conn, cursor = connect()
    insert_historical_data(cursor, days)
    insert_average_data(cursor, days, times)
    conn.commit()
    conn.close()
