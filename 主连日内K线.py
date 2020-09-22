from tqsdk import TqApi
from DataLoader import download_data, read_data
import pandas as pd
from datetime import datetime

api = TqApi()
quotes = api._data["quotes"]

symbol_list = []
for symbol, item in quotes.items():
    if item["ins_class"] == "FUTURE_INDEX":
        print(symbol)
        symbol_list.append(symbol)

print("number of contracts: ", len(symbol_list))

#download_data(symbol_list, datetime(2016,1,1), datetime(2020,8,30), "min")

data = []
cols = []
for symbol in symbol_list:
    symbol = symbol.split('@')[1]
    ds = read_data(symbol, 'min', None, None)
    data.append(ds['close'])
    cols.append(symbol)

df = pd.concat(data, axis = 1)
df.columns = cols
df.to_csv('daily_prices.csv')
correlation = df.corr()

