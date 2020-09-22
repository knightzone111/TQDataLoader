from tqsdk import TqApi
from DataLoader import download_data, read_data
from datetime import datetime

api = TqApi()
quotes = api._data['quotes']

symbols = []
for symbol, item in quotes.items():
    if item['ins_class'] == 'FUTURE':
        symbols.append(symbol)
print(len(symbols))
download_data(symbols[1500:2500], datetime(2016,1,1), datetime(2020,8,25), "tick")
#download_data(symbols, datetime(2016,1,1), datetime(2020,8,25), "D")

