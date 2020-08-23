from tqsdk import TqApi
from DataLoader import download_data, read_data

api = TqApi()
quotes = api._data["quotes"]

symbol_list = []
for symbol, item in quotes.items():
    if item["ins_class"] == "FUTURE_INDEX":
        symbol_list.append(symbol)

print("number of contracts: ", len(symbol_list))

download_data(symbol_list, "2016-01-01", "2020-08-20", "D")