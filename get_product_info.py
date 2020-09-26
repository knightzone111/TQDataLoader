from tqsdk import TqApi
from DataLoader import download_data, read_data
import pandas as pd
from datetime import datetime

api = TqApi()
quotes = api._data["quotes"]


def get_product_info(api:TqApi, symbol):
    q = api.get_quote(symbol)

    product_info = {'class': q.ins_class, 'root': q.product_id, 'symbol': q.instrument_id,
               'short_symbol': q.instrument_id.split(".")[1], 'exchange': q.exchange_id,
               'price_tick': q.price_tick, 'multiplier': q.volume_multiple, 
               'trading_hours': q.trading_time, 'max_limit_order_volume': q.max_limit_order_volume,
               'min_limit_order_volume': q.min_limit_order_volume}

    ds = pd.Series(product_info)
    return ds


def remove_digits_from_str(str):
    out = ""
    for s in str:
        if not s.isdigit():
            out += s 
    return out    

def get_root(symbol):
    return remove_digits_from_str(symbol)

product_dict = {}
for symbol, item in quotes.items():
    if item["ins_class"] == "FUTURE":
        root = get_root(symbol)
        if root not in product_dict:
            product_dict[root] = [symbol]
        else:
            product_dict[root].append(symbol)

#         ds = get_product_info(api, symbol)
#         product_list.append(ds)

def get_futures_products():
    product_dict = {}
    for symbol, item in quotes.items():
        if item["ins_class"] == "FUTURE":
            root = get_root(symbol)
            if root not in product_dict:
                product_dict[root] = [symbol]
            else:
                product_dict[root].append(symbol)
    return product_dict  

print(product_dict)

data = {}
prod_dict = get_futures_products()
for root in prod_dict:
    data[root] = get_product_info(api, prod_dict[root][-1])

df = pd.DataFrame(data)
df = df.transpose()
df.to_csv("ProductInfo.csv")
api.close()