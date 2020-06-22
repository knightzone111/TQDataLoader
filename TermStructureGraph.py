# -*- coding: utf-8 -*-
# Import required libraries
import os

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import DataLoader as dl

# Setup the app
app = dash.Dash(__name__)



syms, relative_map = dl.get_recent_symbols("2020-05-20", "SHFE.rb", 12)
data = {}
for sym in syms:
    data[sym] = dl.read_data(sym, 'D', None, None)

tds = pd.date_range("2020-01-05", "2020-05-21")

prices = {}
for td in tds:
    td = str(td.date())
    price_day = {}
    for sym in syms:
        relative_sym = sym.split('.')[1][:-4]+'!'+ str(relative_map[sym])
        try:
            price_day[relative_sym] = (data[sym].loc[td][sym+'.close'])
        except Exception as inst:
            print(inst)
    if price_day:
        prices[td] = price_day


df = pd.DataFrame(prices)
df = df.transpose()

xlist = df.columns
ylist = df.index
zlist = df.values

# Make 3d graph
fig = go.Figure(data=go.Surface(x=xlist, y=ylist, z=zlist, opacity=0.5, showscale=False))
fig.update_layout(autosize=True,
                   margin=dict(
                       t=5,
                       l=5,
                       b=5,
                       r=5,
                   ),
                   hovermode ='closest',
                   scene =dict(
                       xaxis={
                           "showgrid": True,
                           "title": "",
                           "type": "category",
                           "zeroline": False,
                           "categoryorder": 'array',
                           "categoryarray": list(reversed(xlist))
                       },
                        yaxis={
                       "showgrid": True,
                       "title": "Time",
                       "type": "date",
                        "nticks": 5,
                       "zeroline": False},
                       aspectmode="manual",
                       aspectratio=dict(x=2, y=4, z=2)
                   )
                  )

app.layout = html.Div(
    [
        dcc.Graph(
            id='graph',
            style={'height': '100vh'},
            figure=fig
        )
    ])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
