import sqlite3

def delete_db():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE scripts")

    cursor.execute("DROP TABLE Monday")
    cursor.execute("DROP TABLE Tuesday")
    cursor.execute("DROP TABLE Wednesday")
    cursor.execute("DROP TABLE Thursday")
    cursor.execute("DROP TABLE Friday")

    cursor.execute("DROP TABLE Monday_avg")
    cursor.execute("DROP TABLE Tuesday_avg")
    cursor.execute("DROP TABLE Wednesday_avg")
    cursor.execute("DROP TABLE Thursday_avg")
    cursor.execute("DROP TABLE Friday_avg")

    conn.commit()
    conn.close()