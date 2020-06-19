import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import DataLoader
import os
import glob


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
    dcc.Dropdown(id='freq', options=freq_options, style={'width': "40%"}, value = 'D'),
    dcc.Graph(id = 'price_graph', figure={}),
    dcc.Graph(id = 'volume_graph', figure={}),
])

@app.callback(
    Output(component_id='symbol', component_property = 'options'),
    [Input(component_id='exchanges', component_property='value')]
)
def get_available_symbols(exchanges):
    #print("exchanges:", exchanges)
    all_files = []

    if exchanges is None:
        return []


    for exchange in exchanges:
        ex_files = glob.glob(os.path.join(DEFAULT_DATA_FOLDER, "{0}.*/*_{1}.csv".format(exchange, default_freq)))
        #print("paths:", ex_files)
        all_files.extend(ex_files)

    all_symbols = [os.path.basename(file).split("_")[0] for file in all_files]
    symbol_options = [{"label": symbol, "value": symbol} for symbol in all_symbols]

    return symbol_options


@app.callback(
    Output(component_id='price_graph', component_property='figure'),
    [Input(component_id='exchanges', component_property='value'),
     Input(component_id='symbol', component_property='value'),
     Input(component_id='freq', component_property='value')]
)
def update_price_value(exchanges, symbol, freq):
    if symbol is None:
        return {}
    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, freq, start_dt, end_dt)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df[symbol + '.open'], high=df[symbol + '.high'],
        low=df[symbol + '.low'], close=df[symbol + '.close'],
        increasing_line_color='red', decreasing_line_color='green'
    )])

    fig.update_layout(
        title=symbol + ' ' + 'klines',
        xaxis_rangeslider_visible=False
    )

    return fig


@app.callback(
    Output(component_id='volume_graph', component_property='figure'),
    [Input(component_id='symbol', component_property='value')]
)
def update_volume_value(symbol):
    if symbol is None:
        return {}

    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, 'D', start_dt, end_dt)

    fig_dict=dict({
        'data': [
            {'x': df.index, 'y': df[symbol + '.volume'], 'type': 'bar', 'name': symbol}
        ],
        'layout': {
            'title': symbol + ' volume'
        }
    })
    fig = go.Figure(fig_dict)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
