import sqlite3
import csv
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('stock_analysis.db')
cursor = conn.cursor()

query = "SELECT * FROM alerts WHERE date IN (SELECT DISTINCT date FROM alerts ORDER BY date DESC LIMIT 5);"
cursor.execute(query)
data = cursor.fetchall()

formatted_data = [(date, datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f%z').strftime('%H:%M'), script, round(price, 2), alert) for date, time, script, price, alert in data]

alert_dict = {}
for row in formatted_data:
    date, time, script, price, alert = row
    price = round(price, 2)
    if alert not in alert_dict:
        alert_dict[alert] = {date: [(script, price)]}
    elif date not in alert_dict[alert]:
        alert_dict[alert][date] = [(script, price)]
    else:
        alert_dict[alert][date].append((script, price))

alert_sizes = {}
for key in alert_dict.keys():
    size = 0
    for date in alert_dict[key]:
        size = max(size, len(alert_dict[key][date]))
        alert_sizes[key] = size

csv_filename = 'output.csv'
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    sorted_dates = sorted(list(set(date for companies in alert_dict.values() for date in companies.keys())))
    header_row = ['Alert type'] + sorted_dates
    csv_writer.writerow(header_row)
    
    for alert_type, dates_companies in alert_dict.items():
        csv_writer.writerow([alert_type])
        first_day, second_day, third_day, fourth_day, fifth_day = [], [], [], [], []
        if sorted_dates[0] in dates_companies:
            first_day = dates_companies[sorted_dates[0]]
        if sorted_dates[1] in dates_companies: 
            second_day = dates_companies[sorted_dates[1]]
        if sorted_dates[2] in dates_companies:
            third_day = dates_companies[sorted_dates[2]]
        if sorted_dates[3] in dates_companies:
            fourth_day = dates_companies[sorted_dates[3]]
        if sorted_dates[4] in dates_companies:
            fifth_day = dates_companies[sorted_dates[4]]


        for i in range(alert_sizes[alert_type]):
            csv_row = [""]
            if i < len(first_day):
                csv_row += [first_day[i]]
            else:
                csv_row += [""]
            if i < len(second_day):
                csv_row += [second_day[i]]
            else:
                csv_row += [""]
            if i < len(third_day):
                csv_row += [third_day[i]]
            else:
                csv_row += [""]
            if i < len(fourth_day):
                csv_row += [fourth_day[i]]
            else:
                csv_row += [""]
            if i < len(fifth_day):
                csv_row += [fifth_day[i]]
            else:
                csv_row += [""]
            csv_writer.writerow(csv_row)
