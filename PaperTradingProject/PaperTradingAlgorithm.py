import alpaca as tradeAPI
import os
from dotenv import load_dotenv
import datetime
import pandas_datareader as pdr
import yfinance as yf
from dash import html, Dash, dcc
from dash.dependencies import Input,Output
import keyboard
load_dotenv()

API_KEY_SECRET = os.getenv('API_KEY_SECRET')
API_KEY = os.getenv('API_KEY')

while True:
    if keyboard.is_pressed('q'):
        exit

def trading_algo():
    os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

    api = tradeAPI.REST(API_KEY, API_KEY_SECRET, api_version='v2')
    account = api.get_account()

    return

app = Dash()
app.title = "Stock Selector and Visualization"

app.layout = [html.Div(children=[
    html.H1("Stock Data Visualization Dashboard"),
    html.H4("Please enter the stock name"),
    dcc.Input(id='stockSymbolInput', value='AAPL', type="text"),
    html.Div(id='output-graph')
    ])]
@app.callback(
    Output(component_id='output-graph',
component_property='children'),
[Input(component_id='input', component_property='value')]
)

def update_graph(input_data):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()

    try:
        df = pdr.DataReader(input_data, 'yahoo', start, end)

        graph = dcc.Graph(id="example", figure ={'data':[{'x':df.index, 'y':df.Close, 'type':'line', 'name':{'title':input_data}}],'layout':{'title':input_data}})

    except:
        graph= html.Div('Error retrieving stock data.')

    return graph

if __name__ == '__main__':
    app.run(debug=True)