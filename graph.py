import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import DataLoader

start_dt = '2020-01-08'
end_dt = '2020-06-10'
df = DataLoader.read_data('SHFE.rb2010', 'D', start_dt, end_dt)
print(df)

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='symbol', value='SHFE.rb2010', type='text'),
    dcc.Input(id = 'data_type', value='close', type='text'),
    html.Div(id='price-graph'),
    html.Div(id = 'volume-graph')
])

@app.callback(
    Output(component_id='price-graph', component_property='children'),
    [Input(component_id='symbol', component_property='value'), Input(component_id='data_type', component_property='value')]
)
def update_price_value(symbol, data_type):
    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, 'D', start_dt, end_dt)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df[symbol+'.' + data_type], 'type': 'line', 'name': symbol}
            ],
            'layout': {
                'title': symbol + ' ' + data_type
            }
        }
    )


@app.callback(
    Output(component_id='volume-graph', component_property='children'),
    [Input(component_id='symbol', component_property='value')]
)
def update_volume_value(symbol):
    root = symbol[:-4]
    start_dt = None
    end_dt = None
    df = DataLoader.read_data(symbol, 'D', start_dt, end_dt)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df[symbol+'.volume'], 'type': 'bar', 'name': symbol}
            ],
            'layout': {
                'title': symbol + ' volume'
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)