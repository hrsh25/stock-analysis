import sqlite3

def create():
    conn = sqlite3.connect("stock_analysis.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE scripts(name)")

    cursor.execute("CREATE TABLE Monday(date DATE, time TIME, script TEXT, volume INTEGER)")
    cursor.execute("CREATE TABLE Tuesday(date DATE, time TIME, script TEXT, volume INTEGER)")
    cursor.execute("CREATE TABLE Wednesday(date DATE, time TIME, script TEXT, volume INTEGER)")
    cursor.execute("CREATE TABLE Thursday(date DATE, time TIME, script TEXT, volume INTEGER)")
    cursor.execute("CREATE TABLE Friday(date DATE, time TIME, script TEXT, volume INTEGER)")

    cursor.execute("CREATE TABLE Monday_avg(script TEXT, time TIME, avg_volume INTEGER)")
    cursor.execute("CREATE TABLE Tuesday_avg(script TEXT, time TIME, avg_volume INTEGER)")
    cursor.execute("CREATE TABLE Wednesday_avg(script TEXT, time TIME, avg_volume INTEGER)")
    cursor.execute("CREATE TABLE Thursday_avg(script TEXT, time TIME, avg_volume INTEGER)")
    cursor.execute("CREATE TABLE Friday_avg(script TEXT, time TIME, avg_volume INTEGER)")

    conn.commit()
    conn.close()