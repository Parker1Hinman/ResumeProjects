import alpaca as tradeAPI
import os
from dotenv import load_dotenv
import datetime
import yfinance as yf
from dash import html, Dash
from dash.dependencies import Input,Output
load_dotenv()

API_KEY_SECRET = os.getenv('API_KEY_SECRET')
API_KEY = os.getenv('API_KEY')

def trading_algo():
    os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

    api = tradeAPI.REST(API_KEY, API_KEY_SECRET, api_version='v2')
    account = api.get_account()

    return

app = Dash()
app.title = "Stock Selector and Visualization"

app.layout = [html.Div(children="Hello World")]

if __name__ == '__main__':
    app.run(debug=True)