#To/Do Learn Dash, mess around with graphs
#To/Do connect with stock data
#To/Do create Trading Algorithm

import alpaca as tradeAPI
import os
from dotenv import load_dotenv
import datetime
from alpha_vantage.timeseries import TimeSeries
from dash import html, Dash, dcc, callback, State, Input, Output
import pandas as pd
import plotly.express as px


load_dotenv()

API_KEY_SECRET = os.getenv('API_KEY_SECRET')
API_KEY = os.getenv('API_KEY')

def trading_algo():
    os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

    api = tradeAPI.REST(API_KEY, API_KEY_SECRET, api_version='v2')
    account = api.get_account()

    return

df = pd.read_csv()

app = Dash()

app.title = 'Stock Trading Dashboard'
app.layout = [  html.Div(children=(
                    dcc.Input(id='stockTickerInput',type='text',placeholder='Ex. APPL'))), 
                html.Div(children=(  
                    dcc.Graph(id='stockHistoryGraph')
                ))]

@callback(
    Input('stockTickerInput', 'value'),
    Output('stockHistoryGraph', 'children')
)

def update_graph():
    pass

if __name__ == '__main__':
    app.run(debug=True)