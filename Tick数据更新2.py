from tqsdk import TqApi
from DataLoader import download_data, read_data
from datetime import datetime

api = TqApi()
quotes = api._data['quotes']

symbols = []
for symbol, item in quotes.items():
    if item['ins_class'] == 'FUTURE':
        symbols.append(symbol)
<<<<<<< HEAD
print(len(symbols))
download_data(symbols[1500:2500], datetime(2016,1,1), datetime(2020,8,25), "tick")
=======

<<<<<<< HEAD
print(len(symbols))

download_data(symbols[10:1000], datetime(2016,1,1,0,0), datetime(2020,8,31,0,0), "tick")
=======
download_data(symbols[1000:1500], datetime(2016,1,1), datetime(2020,8,25), "tick")
>>>>>>> 3431b1e158b6ab39b51f776a5bc40985ad3e402b
#download_data(symbols, datetime(2016,1,1), datetime(2020,8,25), "D")

>>>>>>> origin/master
