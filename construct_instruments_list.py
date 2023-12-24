import json
import pandas as pd

df = pd.read_csv('NSE.csv')
data_dict = dict(zip(df['tradingsymbol'], df['instrument_key']))
json_data = json.dumps(data_dict, indent=4)

with open('instruments.json', 'w') as json_file:
    json_file.write(json_data)