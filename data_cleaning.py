import pandas as pd
import os
# use resample to fill the holes.
# for each day, fix the time range and get the specified data.

start_time = "09:00:00"
end_time = "23:59:59"
break1_start = "15:00:00"
break1_end = "20:59:59"

break2_start = ""

start_date = "2020-01-01"
end_date = "2020-08-31"
symbol = "SHFE.rb2101"
freq = 'tick'

DATA_FOLDER_PATH = "C:\\Users\\kzchi\\PycharmProjects\\TQDataLoader\\Data"
CLEAN_FOLDER_PATH = "CleanData"

subfolder_path = "SHFE.rb"
filepath = os.path.join(DATA_FOLDER_PATH, subfolder_path, symbol + '_' + freq + '.csv')

df = pd.read_csv(filepath, index_col=0)
dt_index = pd.to_datetime(df.index)
df.set_index(dt_index, inplace = True)

tds = pd.date_range(start_date, end_date, freq = 'D')

_data = []


def clean_data(df):
    _df = df.resample("s").first().fillna(method = 'ffill')
    return _df


for td in tds:
    start_dt = td.strftime("%F") + ' ' + start_time
    end_dt = td.strftime("%F") + ' ' + end_time
    break_start_dt = td.strftime("%F") + ' ' + break_start
    break_end_dt = td.strftime("%F") + ' ' + break_end

    print(start_dt, end_dt)
    _df = df.loc[start_dt:end_dt]
    _df = _df.drop(_df.loc[break_start_dt:break_end_dt].index)
    print(_df)
    if not _df.empty:
        _df_clean = clean_data(_df)
        _data.append(_df_clean)

df_clean = pd.concat(_data)
clean_subfolder = os.path.join(CLEAN_FOLDER_PATH, subfolder_path)
if not os.path.exists(clean_subfolder):
    os.mkdir(clean_subfolder)

clean_filepath = os.path.join(CLEAN_FOLDER_PATH, subfolder_path, symbol + '_' + freq + '.csv')
df_clean.to_csv(clean_filepath)




