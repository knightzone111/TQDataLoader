from tqsdk import TqApi
from DataLoader import download_data, read_data
from datetime import datetime

api = TqApi()
quotes = api._data['quotes']

symbols = []
for symbol, item in quotes.items():
    if item['ins_class'] == 'FUTURE':
        symbols.append(symbol)
        
download_data(symbols[10:100], datetime(2016,1,1,0,0), datetime(2020,8,31,0,0), "tick")
