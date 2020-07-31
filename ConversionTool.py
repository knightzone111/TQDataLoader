import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# convert GC (price quote 1 troy ounces) to AU(1g)
# 1 troy ounce to 31.1034768 gram
# CNY/USD = 7


app = dash.Dash(__name__)
dcc.Input(placeholder='Base Contract', type='numbers')
dcc.Input(placeholder='Target Contracts', type='numbers')

base_price = 430.80
target_price = 1947.3
measure_unit = 31.1034768
cnyusd = 7

unit_options = {"ounce/g": 31.1034}
currency_options = {"CNY/USD": 7.0}

app.layout = html.Div(
    [html.H1('Conversion Tool')] +
    [
        dcc.Input(id='input_base_price', type='number', placeholder='base contract price'),
        dcc.Input(id='input_target_price', type='number', placeholder='target contract price'),
        dcc.Dropdown(id='input_measure_unit', placeholder='measure exchange', style={'width': "40%"},
                     options=[{"label": label, "value": value} for label, value in unit_options.items()]),
        dcc.Dropdown(id='input_currency_unit', placeholder='currency exchange', style = {'width': "40%"}, options = [{"label": label, "value": value} for label, value in currency_options.items()])
    ]
    + [html.Div(id="converted_base_price")]
)


@app.callback(Output("converted_base_price", "children"),
              [Input("input_base_price", "value"), Input("input_target_price", "value"),
               Input("input_measure_unit", "value"), Input("input_currency_unit", "value")])
def convert_to_base(base_price, target_price, measure_unit, currency):
    """
    convert target contract to base contract
    :param currency: e.g CNY/USD
    :type currency: float
    :param measure_unit: number used to convert target unit into 1 base unit
    :type measure_unit: float
    :param base_price: base contract price
    :type base_price: float
    :param target_price: target contract price
    :type target_price: float
    """

    if base_price and target_price and measure_unit and currency:

        converted_price = target_price / measure_unit * currency
        diff = converted_price - base_price
        print('converted price', 'base price', 'diff')
        return np.round(converted_price, 2)
    else:
        return "Converted Based Price"


# print(convert_to_base(base_price, target_price, measure_unit, cnyusd))

if __name__ == '__main__':
    app.run_server(debug=True)
