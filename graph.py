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

# start_dt = '2020-01-08'
# end_dt = '2020-06-10'
# df = DataLoader.read_data('SHFE.rb2010', 'D', start_dt, end_dt)
# print(df)

app = dash.Dash()
EMPTY_GRAPH = dcc.Graph(id='example-graph', )
files = glob.glob(os.path.join("Data" + "/SHFE.rb/*.csv"))
symbols = [os.path.basename(file).split("_")[0] for file in files]
symbol_options = [{"label": symbol, "value": symbol} for symbol in symbols]

exchange_list = ['SHFE', 'DCE', 'CZCE', 'INE', 'KQ', 'SSWE', 'SSE', 'SZSE']
exchange_options = [{"label": ex, "value": ex} for ex in exchange_list]

# candle stick


app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Checklist(id='exchanges', options=exchange_options),
    dcc.Dropdown(id='symbol', options=symbol_options, style={'width': "40%"}),
    dcc.Input(id='data_type', value='close', type='text'),
    dcc.Input(id='freq', value='D', type='text'),

    html.Button('min', id='min_freq'),
    html.Button('D', id='D_freq'),
    html.Div(id='price-graph'),
    html.Div(id='volume-graph'),
])


@app.callback(
    Output(component_id='price-graph', component_property='children'),
    [Input(component_id='exchanges', component_property='value'),
     Input(component_id='symbol', component_property='value'),
     Input(component_id='data_type', component_property='value'),
     Input(component_id='freq', component_property='value')]
)
def update_price_value(exchanges, symbol, data_type, freq):
    print(exchanges)
    if symbol is None:
        return EMPTY_GRAPH

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
        title=symbol,
        xaxis_rangeslider_visible=False
    )

    return dcc.Graph(
        id='example-graph',
        figure=fig
    )


@app.callback(
    Output(component_id='volume-graph', component_property='children'),
    [Input(component_id='symbol', component_property='value')]
)
def update_volume_value(symbol):
    if symbol is None:
        return EMPTY_GRAPH

    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, 'D', start_dt, end_dt)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df[symbol + '.volume'], 'type': 'bar', 'name': symbol}
            ],
            'layout': {
                'title': symbol + ' volume'
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
