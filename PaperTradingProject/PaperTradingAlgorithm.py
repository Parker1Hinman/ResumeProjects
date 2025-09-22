#To/Do Learn Dash, mess around with graphs
#To/Do connect with stock data
#To/Do create Trading Algorithm

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os
from dotenv import load_dotenv
import datetime
from alpha_vantage.timeseries import TimeSeries
from dash import html, Dash, dcc, callback, State, Input, Output
import pandas as pd
import plotly.express as px


load_dotenv(dotenv_path="ResumeProjects\PaperTradingProject\API_INFO.env")

ALPACA_API_KEY_SECRET = os.getenv('ALPACA_API_KEY_SECRET')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

api = TradingClient(ALPACA_API_KEY, ALPACA_API_KEY_SECRET, paper=True)
account = api.get_account()
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

def purchase(stockTicker, quantity):
    order_data = OrderRequest(
        symbol=stockTicker,
        qty=quantity,
        side=OrderSide.BUY,
        type=OrderType.MARKET,
        time_in_force=TimeInForce.DAY
    )
    api.submit_order(order_data)


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
        html.H3(id="currentCashBalance"),
        dcc.Input(id="quantityInput", type='number',placeholder='Enter Quantity:', style={"height": "20px",
                "fontSize": "16px",
                "marginRight": "10px",
                "width":"120px",
                "TextAlign":"center",
                "margin":"5px"
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
                "width":"120px"})],id="purchaseOptionsPopUp",style={'display':'none'}),
    html.Div(id="purchaseConfirmation", style={
                "textAlign":'center',
                "marginTop": "10px",
                "color": "green",
                "fontWeight": "bold"
                }),
    dcc.Graph(id='stockHistoryGraph')
])

@callback(
    Output('stockHistoryGraph', 'figure'),
    Output('AutoTraderOn/Off', 'children'),
    Output('purchaseOptionsPopUp', 'style'),
    Output('currentCashBalance', 'children'),
    Output('purchaseConfirmation','children', allow_duplicate=True),
    Input('searchConfirmation', 'n_clicks'),
    Input('AutoTraderOn/Off', 'n_clicks'),
    Input('purchaseOptionsButton', 'n_clicks'),
    State('stockTickerInput', 'value'),
    prevent_initial_call=True
)
def update_UI(_, auto_trader_clicks, purchase_clicks,  tickerSymbol):
    button_text = "Trading Algorithm: On " if auto_trader_clicks % 2 == 1 else "Trading Algorithm: Off"
    confirmation_text = ""
    purchase_style = {'display':'flex','alignItems':'center', 'justifyContent':'center'} if purchase_clicks and purchase_clicks > 0 else {'display':'none'}
    if purchase_clicks and purchase_clicks > 0:
        confirmation_text = ""
    try:
        balance_text = f"Account Balance: ${float(account.cash):,.2f}"
    except:
        balance_text = "Balance unavailable"
    # Handle empty or missing ticker
    if not tickerSymbol:
        fig = px.line(title='Please enter a ticker symbol.')
        return fig, button_text, purchase_style, balance_text, confirmation_text

    #Plotting data
    try:
        get_stock_info_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={tickerSymbol}&apikey={ALPHA_VANTAGE_API_KEY}&datatype=csv'
        df = pd.read_csv(get_stock_info_url)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = px.line(df, x='timestamp', y='close', title=f'{tickerSymbol} Closing Prices')
    except Exception as e:
        print(f'Error fetching data: {e}')
        fig = px.line(title=f'Error loading data for {tickerSymbol}')
    return fig, button_text, purchase_style, balance_text, confirmation_text

@callback(
    Output('purchaseConfirmation','children'),
    Output('purchaseOptionsPopUp','style', allow_duplicate=True),
    Input('confirmPurchaseButton','n_clicks'),
    State('quantityInput','value'),
    State('stockTickerInput','value'),
    prevent_initial_call=True
)

def confirm_purchase(n_clicks, quantity, ticker):
    if not quantity or not ticker:
        return "Invalid Purchase Criteria"
    try:
        purchase(ticker,quantity)
        return f"Purchase confirmed: {quantity} shares of {ticker}", {"display":"none"}
    except:
        return "Purchase failed, please check your inputs"

if __name__ == '__main__':
    app.run(debug=True)