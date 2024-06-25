import sqlite3

def delete_db():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS scripts")
    cursor.execute("DROP TABLE IF EXISTS historical_data_avg")
    cursor.execute("DROP TABLE IF EXISTS alerts")

    conn.commit()
    conn.close()

def delete_rows():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM scripts")
    cursor.execute("DELETE FROM historical_data_avg")
    
    conn.commit()
    conn.close()

def delete_alerts():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alerts")

    conn.commit()
    conn.close()