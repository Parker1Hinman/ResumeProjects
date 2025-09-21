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

ALPACA_API_KEY_SECRET = os.getenv('ALPACA_API_KEY_SECRET')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def trading_algo():
    os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

    api = tradeAPI.REST(ALPACA_API_KEY, ALPACA_API_KEY_SECRET, api_version='v2')
    account = api.get_account()

    return
stockTickerInput = ''
get_stock_info = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={stockTickerInput}&apikey{ALPHA_VANTAGE_API_KEY}&datatype=csv'

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