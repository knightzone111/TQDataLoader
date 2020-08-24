from tqsdk import TqApi
from DataLoader import download_data, read_data
import pandas as pd

api = TqApi()
quotes = api._data["quotes"]

symbol_list = []
for symbol, item in quotes.items():
    if item["ins_class"] == "FUTURE_INDEX":
        symbol_list.append(symbol)

print("number of contracts: ", len(symbol_list))

#download_data(symbol_list, "2016-01-01", "2020-08-30", "D")

data = []
cols = []
for symbol in symbol_list:
    symbol = symbol.split('@')[1]
    ds = read_data(symbol, 'D', None, None)
    data.append(ds['close'])
    cols.append(symbol)

df = pd.concat(data, axis = 1)
df.columns = cols

correlation = df.corr()