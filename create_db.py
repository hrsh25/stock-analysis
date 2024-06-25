import sqlite3

def create():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS scripts(name)")
    cursor.execute("CREATE TABLE IF NOT EXISTS historical_data_avg(time TIME, script TEXT, avg_volume INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS alerts(date DATE, time TIME, script TEXT, price INTEGER, alert_type TEXT)")

    conn.commit()
    conn.close()