from DataLoader import download_data
from datetime import datetime

contract_list = ["2010", "2011", "2012", "2101", "2102", "2103", "2104", "2105", "2106", "2107", "2108", "2109"]
sym_list = ["SHFE.rb" + c for c in contract_list]
#data_task = download_data(sym_list, datetime(2020, 1, 1, 0, 0), datetime(2020, 8, 31, 0, 0), 'tick')
#data_task = download_data(['SHFE.rb2010'], datetime(2019, 10, 1, 0, 0), datetime(2020, 1, 31, 0, 0), 'tick')


root = "SHFE.rb"
month_code = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
year_code = ["16", "17", "18", "19", "20", "21"]

sym_list = [root + y + m for y in year_code for m in month_code]
print(sym_list)
data_task = download_data(sym_list, datetime(2016, 1, 1, 0, 0), datetime(2020, 8, 31, 0, 0), 'tick')

#
# def get_contract_duration(symbol):
#     dstr = symbol[-4:]
#     year = int(dstr[:2]) + 2000
#     month = int(dstr[2:])
#     start_dt = datetime(year = year-1, month = month, day = 15)
#     end_dt = datetime(year = year, month = month, day = 15)
#     return start_dt, end_dt
#
#
#
#
# def get_data_per_contract(symbol, cur_dt):
#     start_dt, end_dt = get_contract_duration(symbol)
#     data_task = download_data([symbol], start_dt, cur_dt, 'tick')
#
# get_data_per_contract("SHFE.rb2010", datetime(2020,8,31))