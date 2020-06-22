# -*- coding: utf-8 -*-
# Import required libraries
import os

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

# Setup the app
app = dash.Dash(__name__)

df = pd.read_csv("yield_curve.csv")

xlist = list(df["x"].dropna())
ylist = list(df["y"].dropna())

print(xlist)
print(ylist)
del df["x"]
del df["y"]
#print(df)

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
                   scene =dict(yaxis={
                       "showgrid": True,
                       "title": "Time",
                       "type": "date",
                       "zeroline": False},
                       xaxis={
                           "showgrid": True,
                           "title": "",
                           "type": "category",
                           "zeroline": False,
                           "categoryorder": 'array',
                           "categoryarray": list(reversed(xlist))
                       },
                       aspectmode="manual",
                       aspectratio=dict(x=2, y=4, z=2)
                   )
                  )

app.layout = html.Div(
    [
        dcc.Graph(
            id='graph',
            style={'height': '60vh'},
            figure=fig
        )
    ])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
