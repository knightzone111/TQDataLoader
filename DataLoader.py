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
    :param freq: specify data frequency
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


def read_data(symbol, freq, folderpath=Default_Folder, verbose=False):
    filepath = os.path.join(folderpath, "{0}_{1}.csv".format(symbol, freq))
    if os.path.exists(filepath):
        _df = pd.read_csv(filepath)
        if verbose:
            print(_df)
    else:
        raise Exception("{0} does not exists.".format(filepath))
    return _df


def get_recent_symbols(trade_date, root, count):
    y, m = trade_date.year, trade_date.month
    symbol_list = []
    for i in range(count):
        if m + i <= 12:
            symbol_list.append(root + datetime.date(y, m + i, 15).strftime("%y%m"))
        else:
            symbol_list.append(root + datetime.date(y + 1, (m + i) % 12, 15).strftime("%y%m"))
    return symbol_list


if __name__ == '__main__':

    data_task = download_data(["SHFE.rb2010"], "2020-06-01", "2020-06-02", 'tick', 'Data')
    df = read_data('SHFE.rb2010', 'tick')
    print(df)
