import time
import json
import datetime
import sqlite3

import schedule
import requests
import pytz

from chump import Application


SUDDEN_PRICE_INCREASE = "Sudden Price Increase"
SUDDEN_PRICE_INCREASE_AGAIN = "Sudden Price Increase Again"
SUDDEN_VOLUME_INCREASE = "Sudden Volume Increase"
ONE_POINT_FIVE_TIMES_VOLUME = "1.5 times Volume"
DOUBLE_VOLUME = "Double Volume"
TRIPLE_VOLUME = "Triple Volume"


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
sudden_price = {}

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
    
def insert_alert(curr_time, date, alert_dict, alert_type):
    for name, price in alert_dict.items():
        cursor.execute(f'''
                            INSERT INTO alerts
                            VALUES (?, ?, ?, ?, ?)
                        ''', (date, curr_time, name, price, alert_type))
        conn.commit()

def main():
    now = datetime.datetime.now().astimezone(pytz.timezone('Asia/Kolkata'))
    date = now.date().strftime("%d/%m/%Y")
    rounded_time = get_rounded_time(now)
    sudden_price_increase = ""
    sudden_price_increase_again = ""
    sudden_volume_increase = ""
    one_point_five_times_volume = ""
    double_volume = ""
    triple_volume = ""
    price_dict = {}
    price_again_dict = {}
    vol_dict = {}
    one_point_five_dict = {}
    two_times_dict = {}
    three_times_dict = {}
    if datetime.time(9, 15) <= rounded_time.time() <= datetime.time(15, 30):
        live_data = get_live_data()
        for script in scripts:
            if script not in live_data or script == "BGRENERGY" or script == "BHARATWIRE":
                continue
            curr_vol = live_data[script]['volume']
            curr_price = live_data[script]['price']
            open_price = live_data[script]['open']
            if script in last_vol:
                script_str = script + " ({}, {})".format(round(curr_vol, 2), round(last_vol[script], 2))
                if rounded_time.hour == 9:
                    if curr_vol >= 2 * last_vol[script]:
                        sudden_volume_increase += script_str
                        sudden_volume_increase += " "
                        vol_dict[script] = curr_price
                else:
                    if curr_vol >= 1.35 * last_vol[script]:
                        sudden_volume_increase += script_str
                        sudden_volume_increase += " "
                        vol_dict[script] = curr_price
            last_vol[script] = curr_vol

            if script in last_price:
                if script in sudden_price:
                    if curr_price >= 1.01 * last_price[script]:
                        script_str = script + " ({}, {})".format(curr_price, last_price[script])
                        sudden_price_increase_again += script_str
                        sudden_price_increase_again += " "
                        price_again_dict[script] = curr_price
                else:
                    if curr_price >= 1.0075 * last_price[script]:
                        script_str = script + " ({}, {})".format(curr_price, last_price[script])
                        sudden_price_increase += script_str
                        sudden_price_increase += " "
                        price_dict[script] = curr_price
                        if script not in sudden_price:
                            sudden_price[script] = curr_price
            last_price[script] = curr_price

            cursor.execute(f'''
                SELECT avg_volume
                FROM historical_data_avg
                WHERE script = ? AND time = ?
            ''', (script, rounded_time.time().strftime("%H:%M")))
            avg_volume = cursor.fetchone()[0]
            if not avg_volume:
                print(script)
                continue
            if curr_vol >= 1.5*avg_volume and 1.0125*open_price >= curr_price >= 1.01*open_price and script not in first_alert:
                one_point_five_times_volume += script
                one_point_five_times_volume += " "
                first_alert.append(script)
                one_point_five_dict[script] = curr_price
            
            if curr_vol >= 2*avg_volume and 1.015*open_price >= curr_price >= 1.0125*open_price and script not in second_alert:
                double_volume += script
                double_volume += " "
                second_alert.append(script)
                two_times_dict[script] = curr_price
                
            if curr_vol >= 3*avg_volume and 1.02*open_price >= curr_price >= 1.015*open_price and script not in third_alert:
                triple_volume += script
                triple_volume += " "
                third_alert.append(script)
                three_times_dict[script] = curr_price

        if len(sudden_volume_increase):
            insert_alert(rounded_time, date, vol_dict, SUDDEN_VOLUME_INCREASE)
            user.create_message(title=SUDDEN_VOLUME_INCREASE, message=sudden_volume_increase).send()

        if len(sudden_price_increase):
            insert_alert(rounded_time, date, price_dict, SUDDEN_PRICE_INCREASE)
            user.create_message(title=SUDDEN_PRICE_INCREASE, message=sudden_price_increase).send()

        if len(sudden_price_increase_again):
            insert_alert(rounded_time, date, price_again_dict, SUDDEN_PRICE_INCREASE_AGAIN)
            user.create_message(title=SUDDEN_PRICE_INCREASE_AGAIN, message=sudden_price_increase_again).send()

        if len(one_point_five_times_volume):
            insert_alert(rounded_time, date, one_point_five_dict, ONE_POINT_FIVE_TIMES_VOLUME)
            user.create_message(title=ONE_POINT_FIVE_TIMES_VOLUME, message=one_point_five_times_volume).send()
        
        if len(double_volume):
            insert_alert(rounded_time, date, two_times_dict, DOUBLE_VOLUME)
            user.create_message(title=DOUBLE_VOLUME, message=double_volume).send()
        
        if len(triple_volume):
            insert_alert(rounded_time, date, three_times_dict, TRIPLE_VOLUME)
            user.create_message(title=TRIPLE_VOLUME, message=triple_volume).send()

schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
