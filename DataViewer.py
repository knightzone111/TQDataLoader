import datetime
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

import pandas as pd
from datetime import datetime
import DataLoader
import os
import glob
import dashlib

DEFAULT_DATA_FOLDER = 'Data'
default_freq = 'D'

app = dash.Dash("DataViewer")

# exchange list
exchange_list = ['SHFE', 'DCE', 'CZCE', 'INE', 'KQ', 'SSWE', 'SSE', 'SZSE']
exchange_options = [{"label": ex, "value": ex} for ex in exchange_list]

# frequency
freq_list = ["tick", "s", "min", "5min", "h", "D"]
freq_options = [{"label": f, "value": f} for f in freq_list]


app.layout = html.Div(children=[

    dcc.Checklist(id='exchanges', options=exchange_options, ),
    dcc.Dropdown(id='symbol', options=[], style={'width': "40%"}, placeholder="Symbol"),
    dcc.Dropdown(id='freq', options=freq_options, style={'width': "40%"}, value='D'),
    dcc.Graph(id='price_graph', figure={}),
    dcc.Graph(id='volume_graph', figure={}),
    dcc.Graph(id='oi_graph', figure={}),
    html.H3("Data Summary"),
    dash_table.DataTable(id='summary_table'),

])

@app.callback(
    Output(component_id='symbol', component_property='options'),
    [Input(component_id='exchanges', component_property='value')]
)
def get_available_symbols(exchanges):
    # print("exchanges:", exchanges)
    all_files = []

    if exchanges is None:
        return []

    for exchange in exchanges:
        ex_files = glob.glob(os.path.join(DEFAULT_DATA_FOLDER, "{0}.*/*_{1}.csv".format(exchange, default_freq)))
        all_files.extend(ex_files)

    all_symbols = [os.path.basename(file).split("_")[0] for file in all_files]
    symbol_options = [{"label": symbol, "value": symbol} for symbol in all_symbols]

    return symbol_options

@app.callback(
    [Output(component_id='price_graph', component_property='figure'),
     Output(component_id='summary_table', component_property='columns'),
     Output(component_id='summary_table', component_property='data')],
    [Input(component_id='exchanges', component_property='value'),
     Input(component_id='symbol', component_property='value'),
     Input(component_id='freq', component_property='value')]
)
def update_price_value(exchanges, symbol, freq):
    if symbol is None:
        raise PreventUpdate
    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, freq, start_dt, end_dt)
    df_summary = dashlib.generate_summary_table(df, symbol)
    data = df_summary.to_dict('records')

    columns = [
        {'name': k.capitalize(), 'id': k}
        for k in data[0].keys()
    ]

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df[symbol + '.open'], high=df[symbol + '.high'],
        low=df[symbol + '.low'], close=df[symbol + '.close'],
        increasing_line_color='red', decreasing_line_color='green'
    )])

    fig.update_layout(
        title=symbol + ' ' + 'klines',
        xaxis_rangeslider_visible=True,
        height=600
    )
    return fig, columns, data

@app.callback(
    [Output(component_id='volume_graph', component_property='figure'),
     Output(component_id='oi_graph', component_property='figure')],
    [Input(component_id='symbol', component_property='value')]
)
def update_volume_value(symbol):
    if symbol is None:
        raise PreventUpdate

    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, 'D', start_dt, end_dt)

    volume_fig_dict = dict({
        'data': [
            {'x': df.index, 'y': df[symbol + '.volume'], 'type': 'bar', 'name': symbol}
        ],
        'layout': {
            'title': symbol + ' volume'
        }
    })

    oi_fig_dict = dict({
        'data': [
            {'x': df.index, 'y': df[symbol + '.close_oi']-df[symbol + '.open_oi'], 'type': 'bar', 'name': symbol}
        ],
        'layout': {
            'title': symbol + ' net_oi'
        }
    })

    volume_fig = go.Figure(volume_fig_dict)
    oi_fig_fig = go.Figure(oi_fig_dict)
    return volume_fig, oi_fig_fig


if __name__ == '__main__':
    app.run_server(host="127.0.0.1", port="8060", debug=True)
