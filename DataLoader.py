from tqsdk import TqApi, TqSim
from tqsdk.tools import DataDownloader
from contextlib import closing
import datetime
import os
import pandas as pd

from typing import List

# TODO: GUI - downloading data, dataviewer, volume feature
# TODO: Commandline options

Default_Folder = 'Data'
if not os.path.exists(Default_Folder):
    os.mkdir(Default_Folder)


def download_data(symbol_list: List[str], start_dt: str, end_dt: str, freq: str, folderpath: str = Default_Folder):
    """
    :param symbol_list: a list of symbols
    :type symbol_list: List[str]
    :param start_dt: start date
    :type start_dt: str, datetime
    :param end_dt: end date
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

    api = TqApi(TqSim())
    download_tasks = {}

    root_sym = symbol_list[0][:-4]
    folderpath = os.path.join(folderpath, root_sym)

    if not os.path.exists(folderpath):
        os.mkdir(folderpath)

    for symbol in symbol_list:

        task = "{0}_{1}".format(symbol, freq)
        filepath = os.path.join(folderpath, task + '.csv')
        _start_dt = pd.to_datetime(start_dt)
        _end_dt = pd.to_datetime(end_dt)
        download_tasks[task] = DataDownloader(api, symbol, time_map[freq], _start_dt, _end_dt, filepath)

    with closing(api):
        while not all([v.is_finished() for v in download_tasks.values()]):
            api.wait_update()
            print("progress: ", {k: ("%.2f%%" % v.get_progress()) for k, v in download_tasks.items()})
    return download_tasks


def read_data(symbol, freq, start_dt:str, end_dt:str, folderpath=Default_Folder, verbose=False):
    filepath = os.path.join(folderpath, symbol[:-4], "{0}_{1}.csv".format(symbol, freq))

    if os.path.exists(filepath):
        _df = pd.read_csv(filepath, parse_dates=['datetime'], index_col=0)
        if start_dt in _df.index and end_dt in _df.index:
            _df = _df[start_dt:end_dt]
        else:
            if start_dt not in _df.index:
                raise Exception("{0} is not in the dataset.".format(start_dt))
            if end_dt not in _df.index:
                raise Exception("{0} is not in the dataset.".format(end_dt))

        if verbose:
            print(_df)
    else:
        raise Exception("{0} does not exists.".format(filepath))
    return _df


def get_recent_symbols(trade_date: datetime.date, root: str, count: int):
    y, m = trade_date.year, trade_date.month
    symbol_list = []
    for i in range(count):
        if m + i <= 12:
            symbol_list.append(root + datetime.date(y, m + i, 15).strftime("%y%m"))
        else:
            symbol_list.append(root + datetime.date(y + 1, (m + i) % 12, 15).strftime("%y%m"))
    return symbol_list


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
        _data.append((symbol, _df[symbol+'.{0}'.format(data_type)].mean()))
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

if __name__ == '__main__':

    #data_task = download_data(["SHFE.rb2010"], "2020-06-01", "2020-06-02", 'tick', 'Data')
    #df = read_data('SHFE.rb2010', 'tick')
    #print(df)

    symlist = get_recent_symbols(datetime.date(2020,6,4), 'SHFE.hc',12)
    #data_task = download_data(symlist, "2020-05-25", "2020-06-03", 'D')
    #df_vol = group_view(symlist, 'volume', "2020-05-26", "2020-06-03")
    #print(df_vol)
    import matplotlib.pyplot as plt
    #df_vol.plot(kind = 'bar')
    #plt.show()

    df_view = quick_view("SHFE.hc","volume","2020-06-03")
    print(df_view)
    df_view.plot(kind = 'bar')
    plt.show()