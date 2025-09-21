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
    html.Div([
        html.Div([
            html.H1('Stock Look Up', style={
                "lineHeight": "1.25",
                "fontSize": "32px",
                "letterSpacing": ".08em",
                "textTransform": "uppercase",
                "margin": "0",
                "paddingRight": "20px"
            }),
            dcc.Input(id='stockTickerInput', type='text', placeholder='Ex. AAPL', style={
                "height": "20px",
                "fontSize": "16px",
                "marginRight": "10px"
            }),
            html.Button('Search', id='searchConfirmation', n_clicks=0, style={
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
                "transition": "background-color .6s ease",
                "margin": "5px"
            }), 
            html.Button('Purchase Options', id="purchaseOptionsButton", n_clicks=0, style={
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
                "transition": "background-color .6s ease",
                "margin": "5px",
            }), 
            html.Button('Trading Algorithm: Off', id='AutoTraderOn/Off', n_clicks=0, style={
                "padding": "5px 10px",
                "borderRadius": "3px",
                "boxShadow": "0px 0px 12px -2px rgba(0,0,0,0.5)",
                "lineHeight": "1.25",
                "width": "290px",
                "background": "black",
                "color": "white",
                "fontSize": "16px",
                "letterSpacing": ".08em",
                "textTransform": "uppercase",
                "position": "relative",
                "transition": "background-color .6s ease",
                "margin": "5px"
            })
        ], style={"display": "flex", "alignItems": "center"})
    ], style={
        "display": "flex",
        "alignItems": "center",
        "marginBottom": "10px"
    }),
    html.Div([
        dcc.Input(id="quantityInput", type='number',placeholder='Enter Quantity:', style={"height": "20px",
                "fontSize": "16px",
                "marginRight": "10px",
                "width":"120px",
                "TextAlign":"center"
                }),
        html.Button("Confirm",id="confirmPurchaseButton", style={"padding": "5px 10px",
                "borderRadius": "3px",
                "boxShadow": "0px 0px 12px -2px rgba(0,0,0,0.5)",
                "lineHeight": "1.25",
                "background": "black",
                "color": "white",
                "fontSize": "16px",
                "letterSpacing": ".08em",
                "textTransform": "uppercase",
                "position": "relative",
                "margin": "5px",
                "width":"120px"})
                ],id="purchaseOptionsPopUp",style={'display':'none'}),
    dcc.Graph(id='stockHistoryGraph')
])

@callback(
    Output('stockHistoryGraph', 'figure'),
    Output('AutoTraderOn/Off', 'children'),
    Output('purchaseOptionsPopUp', 'style'),
    Input('searchConfirmation', 'n_clicks'),
    Input('AutoTraderOn/Off', 'n_clicks'),
    Input('purchaseOptionsButton', 'n_clicks'),
    State('stockTickerInput', 'value')
)
def update_UI(_, auto_trader_clicks, purchase_clicks, tickerSymbol):
    button_text = "Trading Algorithm: On " if auto_trader_clicks % 2 == 1 else "Trading Algorithm: Off"

    purchase_style = {'display':'flex','alignItems':'center', 'justifyContent':'center'} if purchase_clicks and purchase_clicks > 0 else {'display':'none'}
    # Handle empty or missing ticker
    if not tickerSymbol:
        fig = px.line(title='Please enter a ticker symbol.')
        return fig, button_text, purchase_style

    #Plotting data
    try:
        get_stock_info_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={tickerSymbol}&apikey={ALPHA_VANTAGE_API_KEY}&datatype=csv'
        df = pd.read_csv(get_stock_info_url)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = px.line(df, x='timestamp', y='close', title=f'{tickerSymbol} Closing Prices')
    except Exception as e:
        print(f'Error fetching data: {e}')
        fig = px.line(title=f'Error loading data for {tickerSymbol}')
    return fig, button_text

@callback(
    Output('purchaseConfirmation','children'),
    Input('confirmPurchaseButton','n_clicks'),
    State('quantityInput','value')
    State('stockTickerInput','value')
)

def confirm_purchase(n_clicks, quantity, ticker):
    if not quantity or not ticker:
        return "Invalid Purchase Criteria"
    return f"Purchase confirmed: {quantity} shares of {ticker}"

if __name__ == '__main__':
    app.run(debug=True)