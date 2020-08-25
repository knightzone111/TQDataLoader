from tqsdk import TqApi, TqSim
#from tqsdk.tools import DataDownloader
from tqdownloader import DataDownloader
from contextlib import closing
from datetime import datetime, timedelta, date
import os
import pandas as pd
from dateutil.relativedelta import relativedelta


from typing import List

# TODO: GUI - downloading data, dataviewer, volume feature
# TODO: Commandline options

Default_Folder = 'Data'
if not os.path.exists(Default_Folder):
    os.mkdir(Default_Folder)

def download_data(symbol_list: List[str], start_dt: datetime, end_dt: datetime, freq: str):
    """
    :param symbol_list: a list of symbols
    :type symbol_list: List[str]
    :param start_dt: start date, default time of the day is 08:00
    :type start_dt: str, datetime
    :param end_dt: end date, default time of the day is 08:00
    :type end_dt: str, datetime
    :param freq: one of the data frequency, "tick", "s", "min", "5min", "h", "D"
    :type freq: str
    :param folderpath: folder path of the downloaded data
    :type folderpath: str
    :return: A dict of DataDownloader object with get_progress and is_Finished method.
    :rtype: Dict[str, DataDownloader]
    """
    time_map = {"tick": 0, "s": 1, "min": 60, "5min": 5 * 60, "h": 3600, "D": 24 * 3600}
    if freq not in time_map:
        raise Exception("freq entered is not in the time_map.")

    _start_dt = start_dt
    _end_dt = end_dt
    if start_dt > end_dt:
        raise Exception("Start time has to be earlier than the end datetime.")

    api = TqApi(TqSim())

    download_tasks = {}
    # create root folder
    for symbol in symbol_list:
        if symbol.split("@")[0] == 'KQ.i':
            root_sym = symbol.split("@")[1]
            subfolder = os.path.join(Default_Folder, root_sym)
            task_name = "{0}_{1}".format(root_sym, freq)

        else:
            root_sym = symbol[:-4]
            subfolder = os.path.join(Default_Folder, root_sym)
            task_name = "{0}_{1}".format(symbol, freq)

        if not os.path.exists(subfolder):
            os.mkdir(subfolder)

        filepath = os.path.join(subfolder, task_name + ".csv")

        if task_name not in download_tasks:
            try:
                # create download task
                download_tasks[task_name] = DataDownloader(api, symbol, time_map[freq], _start_dt, _end_dt, filepath)
            except Exception as inst:
                print(inst)

    with closing(api):
        while not all([v.is_finished() for v in download_tasks.values()]):
            api.wait_update()
            print("progress: ", {k: ("%.2f%%" % v.get_progress()) for k, v in download_tasks.items()})
    return download_tasks


def read_data(symbol, freq: str, start_dt: str, end_dt: str, verbose=False):

    if not symbol[-4:].isdigit(): # 最后四位若不是数字,则是主连
        root_sym = symbol
        task_name = "{0}_{1}".format(root_sym, freq)

    else:
        root_sym = symbol[:-4]
        task_name = "{0}_{1}".format(symbol, freq)

    filepath = os.path.join(Default_Folder, root_sym, "{0}.csv".format(task_name))
    print(filepath)
    if os.path.exists(filepath):

        data = pd.read_csv(filepath, index_col="datetime")
        data.index = pd.DatetimeIndex(data.index) # convert string date into datetime
        data = data[~data.index.duplicated(keep='first')] # remove duplicated index
        _df = data.dropna()

        if start_dt is None and end_dt is None:
            return _df

        _df = _df[start_dt:end_dt]

        if verbose:
            print(_df)
    else:
        raise Exception("{0} does not exists.".format(filepath))
    return _df


def get_fm_date(cur_date, settlement_day, relative_month=1):
    ct_year, ct_mon, ct_day = cur_date.year, cur_date.month, cur_date.day
    if ct_day < settlement_day:
        fm_date = cur_date
    else:
        fm_date = cur_date + relativedelta(months=relative_month)
    return fm_date


def get_recent_symbols(trade_date, root: str, count: int, settlement_day: int = 15):
    trade_date = pd.to_datetime(trade_date).date()
    contract_dates = []
    symbol_list = []
    relative_map = {}

    fm = get_fm_date(trade_date, settlement_day)

    for i in range(count):
        contract_date = fm + relativedelta(months=i)
        contract_dates.append(contract_date)

        sym = root + contract_date.strftime("%y%m")
        symbol_list.append(sym)
        relative_map[sym] = i


    return symbol_list, relative_map


def group_view(symbol_list: List[str], data_type: str, start_dt: str, end_dt: str):
    """
    For comparing different contracts statistics.
    :param symbol_list: a list of string
    :type symbol_list: List[str]
    :param data_type: open, high, low, close, volume, open_oi, close_oi
    :type data_type: str
    :param start_dt: string of start date
    :type start_dt: string
    :param end_dt: string of end date
    :type end_dt: str
    :return: a dataframe with index of symbols
    :rtype: pd.DataFrame
    """
    _data = []
    for symbol in symbol_list:
        _df = read_data(symbol, 'D', start_dt, end_dt)
        _data.append((symbol, _df[symbol + '.{0}'.format(data_type)].mean()))
    df_data = pd.DataFrame(_data, columns=['symbol', data_type])
    df_data.set_index('symbol', inplace=True)
    return df_data


def quick_view(root: str, data_type: str, trade_date: str) -> pd.DataFrame:
    """
    view data on the trade_date
    :param root:
    :type root:
    :param data_type:
    :type data_type:
    :param trade_date:
    :type trade_date:
    :return:
    :rtype:
    """
    trade_date = pd.to_datetime(trade_date).date()
    symlist = get_recent_symbols(trade_date, root, 12)
    df_data = group_view(symlist, data_type, trade_date, trade_date)
    return df_data


def quick_daily_data_download(root_list):
    for root in root_list:
        today = datetime.now()
        symlist = get_recent_symbols(today, root, 12)
        start_dt = today - timedelta(days=360)
        download_data(symlist, start_dt, today, 'D')



if __name__ == '__main__':
    # data_task = download_data(["SHFE.rb2010","SHFE.ni2008", "SHFE.ni2009", ], "2020-01-01", "2020-06-11", 'D')
    # df = read_data('SHFE.rb2010', 'D', "2020-01-10", "2020-06-02")
    # print(df)

    #symlist = get_recent_symbols("2020.06.01", 'SHFE.au', 4)
    #print(symlist)

    data_task = download_data(['SHFE.au2012'], datetime(2020,8,7,0,0), datetime(2020,8,11,0,0), 'tick')
    #data_task = download_data(['SHFE.ni2010'], "2020-07-29", "2020-07-31", 'tick')


    # #append新数据
    # datas = datas.append(klines)
    # #去重
    # data = datas[~datas.index.duplicated(keep='first')]
    # #保存
    # data.to_csv("xxx.csv")
    # df_vol = group_view(symlist, 'volume', "2020-05-26", "2020-06-03")
    # print(df_vol)
    # import matplotlib.pyplot as plt
    # df_vol.plot(kind = 'bar')
    # plt.show()

    # df_view = quick_view("SHFE.hc","volume","2020-06-03")
    # print(df_view)
    # df_view.plot(kind = 'bar')
    # plt.show()

    # quick_daily_data_download(['DCE.jm'])
