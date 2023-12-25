import time
import math
import json
import sqlite3
import datetime

import schedule
import requests
import pytz
from chump import Application

conn = sqlite3.connect('stock_analysis.db')
cursor = conn.cursor()
cursor.execute(f'SELECT * FROM scripts')
rows = cursor.fetchall()
scripts = []
for row in rows:
    scripts.append(row[0])

last_price = {}
last_vol = {}
first_alert = []
second_alert = []
third_alert = []
today = datetime.date.today().strftime("%A")

f = open('instruments.json', 'r')
instruments = json.load(f)
f.close()

f = open('./config.json', "r+")
config_data = json.load(f)
access_token = config_data['access_token']
token = config_data['token']
user_id = config_data['user']
f.close()

app = Application(token)
user = app.get_user(user_id)

def get_rounded_time(now):
    current_minute = now.minute
    if current_minute < 15:
        now = now.replace(minute=0)
    elif current_minute < 30:
        now = now.replace(minute=30)
    elif current_minute < 45:
        now = now.replace(minute=30)
    else:
        now = now.replace(minute=0)
        now += datetime.timedelta(hours=1)
    return now

def get_instruments():
    symbols = ''
    for i in range(len(scripts)):
        symbols += instruments[scripts[i]]
        if i < len(scripts) - 1:
            symbols += ','
    return symbols

def get_live_data():
    url = "https://api-v2.upstox.com/market-quote/quotes"
    headers = {
        'accept' : 'application/json',
        'Api-Version': '2.0',
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'symbol': get_instruments(),
        'interval': '1m'
        }

    response = requests.get(url=url, headers=headers, params=params).json()
    response = response['data']
    live_data = {}
    for company, data in response.items():
        live_data[data['symbol']] = {'open': data['ohlc']['open'],
                              'price': data['last_price'],
                              'volume': data['volume']}
    return live_data
    

def main():
    now = datetime.datetime.now().astimezone(pytz.timezone('Asia/Kolkata'))
    # now = datetime.datetime.now().time().strftime('%H:%M')
    rounded_time = get_rounded_time(now)
    sudden_price_increase = ""
    sudden_volume_increase = ""
    one_point_five_times_volumes = ""
    double_volume = ""
    triple_volume = ""
    if datetime.time(9, 15) <= rounded_time.time() <= datetime.time(15, 30):
        live_data = get_live_data()
        for script in scripts:
            curr_vol = live_data[script]['volume']
            curr_price = live_data[script]['price']
            open_price = live_data[script]['open']
            
            if script in last_price:
                if curr_price >= 1.0075 * last_price[script]:
                    sudden_price_increase += script
                    sudden_price_increase += " "
            last_price[script] = curr_price

            if script in last_vol:
                if rounded_time.hour == 9:
                    if curr_vol >= 2 * last_vol[script]:
                        sudden_volume_increase += script
                        sudden_volume_increase += " "
                else:
                    if curr_vol >= 1.2 * last_vol[script]:
                        sudden_volume_increase += script
                        sudden_volume_increase += " "
            last_vol[script] = curr_vol
            cursor.execute(f'''
                SELECT avg_volume
                FROM {today}_avg
                WHERE script = ? AND time = ?
            ''', (script, rounded_time.time().strftime("%H:%M")))
            rows = cursor.fetchone()
            avg_volume = math.ceil(rows[0])

            if curr_vol >= 1.5*avg_volume and 1.0125*open_price <= curr_price <= 1.01*open_price and script not in first_alert:
                one_point_five_times_volumes += script
                one_point_five_times_volumes += " "
                first_alert.append(script)
            
            if curr_vol >= 2*avg_volume and 1.015*open_price <= curr_price <= 1.0125*open_price and script not in second_alert:
                double_volume += script
                double_volume += " "
                second_alert.append(script)
                
            if curr_vol >= 3*avg_volume and 1.02*open_price <= curr_price <= 1.015*open_price and script not in third_alert:
                triple_volume += script
                triple_volume += " "
                third_alert.append(script)

        if len(sudden_price_increase):
            user.create_message(title="Sudden Price Increase", message=sudden_price_increase).send()
        
        if len(sudden_volume_increase):
            user.create_message(title="Sudden Volume Increase", message=sudden_volume_increase).send()

        if len(one_point_five_times_volumes):
            user.create_message(title="1.5 times volume", message=one_point_five_times_volumes).send()
        
        if len(double_volume):
            user.create_message(title="2 times volume", message=double_volume).send()
        
        if len(triple_volume):
            user.create_message(title="3 times volume", message=triple_volume).send()


# main()
schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
