from tqsdk import TqApi
from DataLoader import download_data, read_data

api = TqApi()
quotes = api._data['quotes']

symbols = []
for symbol, item in quotes.items():
    if item['ins_class'] == 'FUTURE':
        symbols.append(symbol)

download_data(symbols, "2016-01-01", "2020-08-25", "tick")
