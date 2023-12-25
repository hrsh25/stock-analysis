import json
import requests
import urllib.parse
import streamlit as st

def generate(code):
    # f = open('./config.json', "r+")
    # config = json.load(f)
    url = "https://api-v2.upstox.com/login/authorization/token"
    headers = {
        'accept' : 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'code': code,
        'client_id': st.secrets['api_key'],
        'client_secret': st.secrets['api_secret'],
        'redirect_uri': st.secrets['rurl'],
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, headers=headers, data=data)
    json_response = response.json()
    st.write(json_response)
    try:
        st.secrets["access_token"] = json_response['access_token']
        # f.seek(0)
        # f.write(json.dumps(config, indent=4))
        st.write("Access Token generated")

    except Exception as e:
        st.error(e)
    st.session_state.token = ""

# rurl = urllib.parse.quote('https://127.0.0.1:5000', safe='')

def get_data():
    f = open('./config.json', "r+")
    data = json.load(f)
    access_token = data['access_token']
    url = "https://api-v2.upstox.com/market-quote/quotes"
    headers = {
        'accept' : 'application/json',
        'Api-Version': '2.0',
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'symbol': 'NSE_EQ|INE046A01015,NSE_EQ|INE795G01014',
        'interval': '1d'
        }

    response = requests.get(url=url, headers=headers, params=params).json()
    response = response['data']
    live_data = {}
    for company, data in response.items():
        live_data[data['symbol']] = {'open': data['ohlc']['open'],
                              'price': data['last_price'],
                              'volume': data['volume']}
    print(live_data)


# code = st.text_input("Enter Code Here: ", key = "code", placeholder="code")
# btn = st.button("Generate", on_click=generate, args=(code,))
# btn2 = st.button("Load", on_click=get_data)