import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

def generate_summary_table(df, sym):
    df_summary = pd.DataFrame({}, index=[sym])
    ndays = len(df)
    price_chg = df['close'] - df['open']
    price_rng = df['high'] - df['low']
    df_summary['ndays'] = ndays
    df_summary['avg_price_chg'] = round(price_chg.mean(),2)
    df_summary['HHigh_chg'] = round(price_chg.max(),2)
    df_summary['LLow_chg'] = round(price_chg.min(),2)
    df_summary['avg_price_rng'] = round(price_rng.mean(),2)
    df_summary['HHigh_rng'] = round(price_rng.max(),2)
    df_summary['LLow_rng'] = round(price_rng.min(),2)
    df_summary['price_std'] = round(df['close'].std(),2)
    df_summary['rng_std'] = round(price_rng.std(),2)
    df_summary['avg_volume'] = round(df['volume'].mean(),2)
    df_summary['avg_open_oi'] = round(df['open_oi'].mean(),2)
    df_summary['avg_close_oi'] = round(df['close_oi'].mean(),2)

    return df_summary
