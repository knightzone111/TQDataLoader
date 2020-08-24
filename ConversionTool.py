import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

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
cnyusd = 6.92


unit_options = {"ounce/g": 31.1034}
currency_options = {"CNY/USD": 7.0}
pair_options = {"GC-au":"GC-au"}
app.layout = html.Div(
    [html.H1('Conversion Tool')] +
    [
        dcc.Dropdown(id = 'converting_pair', placeholder='Choosing Contract Pairs', style = {'width':'60%'},
                     options = [{'label': label, "value": value} for label, value in pair_options.items()]),
        dcc.Input(id='input_measure_unit'),
        dcc.Input(id='input_currency_unit'),
        html.H3("Input Prices:"),
        dcc.Input(id='input_target_price', type='number', placeholder='target contract price'),
        dcc.Input(id='input_base_price', type='number', placeholder='base contract price'),
        dcc.Input(id = 'target_premium', type = 'number', placeholder='target_premium')

    ] +
        [html.H3("Result:"), html.Label("Converted Target Price:"), html.Div(id="converted_target_price"), html.Label("Diff(Target-Base):"), html.Div(id = 'diff_target_base_price')]

)

@app.callback(
    [Output("input_measure_unit", "value"),
     Output("input_currency_unit", "value")],
    [Input("converting_pair", "value")]
)
def pair_dropdown_action(converting_pair):
    if converting_pair == "GC-au":
        measure_unit = "ounce/g"
        currency = "CNY/USD"
        return measure_unit, currency
    else:
        raise PreventUpdate


@app.callback([Output("converted_target_price", "children"),
               Output("diff_target_base_price", "children")],
              [Input("converting_pair", "value"), Input("input_target_price", "value"), Input("input_base_price", "value"), Input("target_premium", "value")])
def convert_to_base(pair, target_price, base_price, target_premium):
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

    if pair and base_price and target_price:
        if pair == "GC-au":
            measure_unit = unit_options["ounce/g"]
            currency = currency_options["CNY/USD"]
        else:
            raise PreventUpdate
        if not target_premium:
            target_premium = 0
        converted_price = contract_convert(target_price, measure_unit, currency)
        diff = converted_price - base_price - target_premium
        # print('converted price', 'base price', 'diff')
        return round(converted_price, 2), round(diff,2)
    else:
        raise PreventUpdate


def contract_convert(target_price, measure_unit, currency):
    return target_price / measure_unit * currency

# print(convert_to_base(base_price, target_price, measure_unit, cnyusd))

if __name__ == '__main__':
    app.run_server(debug=True)
