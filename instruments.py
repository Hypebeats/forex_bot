import requests
import defs
import pandas as pd

session = requests.Session()

url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
#print (url)

response = session.get(url, params=None, headers=defs.SECURE_HEADER)
response.status_code
#print (response.status_code)

data = response.json()
data.keys()

instruments = data['instruments']
instruments[0].keys()

instrument_data = []
for item in instruments:
    new_ob = dict(
        name = item['name'],
        type = item['type'],
        displayPrecision = item['displayPrecision'],
        pipLocation = item['pipLocation'],
        marginRate = item['marginRate']
    )
    instrument_data.append(new_ob)

for item in instrument_data[:3]:
    print(item)

instruments_df = pd.DataFrame.from_dict(instrument_data)
print(instruments_df)

instruments_df.to_pickle('instruments.pkl')
new_table = pd.read_pickle('instruments.pkl')
print(new_table)

