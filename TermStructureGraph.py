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

def get_term_structure_df(current_date:str, start_date:str, end_date:str, root:str, num_contracts:int):
    prices = {}
    syms, relative_map = dl.get_recent_symbols(current_date, root, num_contracts)

    data = {}
    for sym in syms:
        data[sym] = dl.read_data(sym, 'D', None, None)

    tds = pd.date_range(start_date, end_date)

    skipped_days = set({})

    for td in tds:
        td = str(td.date())
        price_day = {}
        for sym in syms:
            relative_sym = sym.split('.')[1][:-4] + '!' + str(relative_map[sym])
            try:
                price_day[relative_sym] = (data[sym].loc[td][sym + '.close'])
            except Exception as inst:
                #print(inst)
                if inst not in skipped_days:
                    skipped_days.add(inst)
                else:
                    continue
        if price_day:
            prices[td] = price_day
    print(skipped_days)
    _df = pd.DataFrame(prices)
    df = _df.transpose()
    return df


# Make 3d graph
def create_term_structure_fig(df):
    xlist = df.columns
    ylist = df.index
    zlist = df.values
    fig = go.Figure(data=go.Surface(x=xlist, y=ylist, z=zlist, opacity=0.7, showscale=False))
    fig.update_layout(autosize=True,
                      margin=dict(
                          t=5,
                          l=5,
                          b=5,
                          r=5,
                      ),
                      hovermode='closest',
                      scene=dict(
                          xaxis={
                              "showgrid": True,
                              "title": "",
                              "type": "category",
                              "zeroline": False,
                              "categoryorder": 'array',
                              "nticks": 12,
                              "categoryarray": list(reversed(xlist))
                          },
                          yaxis={
                              "showgrid": True,
                              "title": "Time",
                              "type": "date",
                              "nticks": 5,
                              "zeroline": False},

                          zaxis={
                              "showgrid": True,
                              "title": "Daily Close",
                              "zeroline": False},
                          aspectmode="manual",
                          aspectratio=dict(x=2, y=4, z=2)
                      )
                      )
    return fig


df = get_term_structure_df("2020-06-10", "2019-01-05", "2020-06-10", "SHFE.hc", 12)
fig = create_term_structure_fig(df)

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
