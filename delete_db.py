import sqlite3

def delete_db():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS scripts")

    cursor.execute("DROP TABLE IF EXISTS Monday")
    cursor.execute("DROP TABLE IF EXISTS Tuesday")
    cursor.execute("DROP TABLE IF EXISTS Wednesday")
    cursor.execute("DROP TABLE IF EXISTS Thursday")
    cursor.execute("DROP TABLE IF EXISTS Friday")

    cursor.execute("DROP TABLE IF EXISTS Monday_avg")
    cursor.execute("DROP TABLE IF EXISTS Tuesday_avg")
    cursor.execute("DROP TABLE IF EXISTS Wednesday_avg")
    cursor.execute("DROP TABLE IF EXISTS Thursday_avg")
    cursor.execute("DROP TABLE IF EXISTS Friday_avg")

    conn.commit()
    conn.close()