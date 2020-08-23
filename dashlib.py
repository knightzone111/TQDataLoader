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
    df_summary['avg_price_chg'] = price_chg.mean().round(2)
    df_summary['HHigh_chg'] = price_chg.max().round(2)
    df_summary['LLow_chg'] = price_chg.min().round(2)
    df_summary['avg_price_rng'] = price_rng.mean().round(2)
    df_summary['HHigh_rng'] = price_rng.max().round(2)
    df_summary['LLow_rng'] = price_rng.min().round(2)
    df_summary['price_std'] = df['close'].std().round(2)
    df_summary['rng_std'] = price_rng.std().round(2)
    df_summary['avg_volume'] = df['volume'].mean().round(2)
    df_summary['avg_open_oi'] = df['open_oi'].mean().round(2)
    df_summary['avg_close_oi'] = df['close_oi'].mean().round(2)

    return df_summary
