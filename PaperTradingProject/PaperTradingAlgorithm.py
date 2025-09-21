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

app = Dash()

app.title = 'Stock Trading Dashboard'
app.layout = html.Div([
                    dcc.Input(id='stockTickerInput',type='text',placeholder='Ex. APPL', style = {"padding":'5px', 'border-radius':'3px', }),
                    html.Button('Search',id='searchConfirmation', n_clicks=0, style={
        "padding": "5px 10px",
        "borderRadius": "3px",
        "boxShadow": "0px 0px 12px -2px rgba(0,0,0,0.5)",
        "lineHeight": "1.25",
        "background": "black",
        "color": "white",
        "fontSize": "16px",
        "letterSpacing": ".08em",
        "textTransform": "uppercase",
        "position": "relative",
        "transition": "background-color .6s ease"
    }
) ,
                    dcc.Graph(id='stockHistoryGraph')
                    ])

@callback(
    Output('stockHistoryGraph', 'figure'),
    Input('searchConfirmation', 'n_clicks'),
    State('stockTickerInput', 'value')
)

def update_graph(_,tickerSymbol):
    get_stock_info_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={tickerSymbol}&apikey={ALPHA_VANTAGE_API_KEY}&datatype=csv'
    try:
        df = pd.read_csv(get_stock_info_url)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = px.line(df, x='timestamp', y='close', title=f'{tickerSymbol} Closing Prices')
        return fig
    except Exception as e:
        if df.shape[1] == 1 and 'Thank you for using Alpha Vantage' in df.columns[0]:
            print("Rate limit exceeded.")
        else:
            print(f'Error fetching data: {e}')
            return px.line(title=f'Error loading data for {tickerSymbol}')

if __name__ == '__main__':
    app.run(debug=True)