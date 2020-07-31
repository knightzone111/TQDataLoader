import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


df = pd.read_csv('Data/SHFE.bu/SHFE.bu2006_D.csv')
def generate_summary_table(df, sym):

    df_summary = pd.DataFrame({}, index = [sym])
    ndays = len(df)
    price_chg = df[sym+'.close']-df[sym +'.open']
    price_rng = df[sym +'.high']-df[sym + '.low']
    df_summary['ndays'] = ndays
    df_summary['avg_price_chg'] = price_chg.mean().round(2)
    df_summary['HHigh_chg'] = price_chg.max().round(2)
    df_summary['LLow_chg'] = price_chg.min().round(2)
    df_summary['avg_price_rng'] = price_rng.mean().round(2)
    df_summary['HHigh_rng'] = price_rng.max().round(2)
    df_summary['LLow_rng'] = price_rng.min().round(2)
    df_summary['price_std'] = df[sym + '.close'].std().round(2)
    df_summary['rng_std'] = price_rng.std().round(2)
    df_summary['avg_volume'] = df[sym +'.volume'].mean().round(2)
    df_summary['avg_open_oi'] = df[sym + '.open_oi'].mean().round(2)
    df_summary['avg_close_oi'] = df[sym + '.close_oi'].mean().round(2)


    return df_summary

df_s = generate_summary_table(df, "SHFE.bu2006")
#print(df_s.to_dict('records'))