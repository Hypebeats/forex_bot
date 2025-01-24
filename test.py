import requests
import defs 
import pandas as pd

session = requests.Session()

instrument = "GBP_USD"
count = 10
granularity = "H1"

url = f"{defs.OANDA_URL}/instruments/{instrument}/candles?count={count}&granularity={granularity}"

params = dict (
    count = count,
    granularity = granularity,
    price = "MBA"
)

response = session.get(url, params=params, headers=defs.SECURE_HEADER)

response.status_code
response.json()

data = response.json()
data.keys()

len(data['candles'])

#insturment data
prices = ['mid', 'bid', 'ask']
ohlc = ['o', 'h', 'l', 'c']

for price in prices :
    for oh in ohlc:
        (f'{price}_{oh}')

data['candles'][0] #data['candles'][0]['mid']['o']

#shows the data for certain instrument
our_data = []
for candle in data['candles']:
    if candle['complete'] == False:
        continue
    new_dict = {}
    new_dict['time'] = candle['time']
    new_dict['volume'] = candle['volume']
    for price in prices:
        for oh in ohlc:
            new_dict[f'{price}_{oh}'] = candle[price][oh]
    our_data.append(new_dict)
print(our_data)

candles_df = pd.DataFrame.from_dict(our_data)
print (candles_df)

candles_df.to_pickle('GBP_USD_H1.pkl')
test_df = pd.read_pickle('GBP_USD_H1.pkl')
print(test_df) 







        










