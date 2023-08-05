import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import yfinance as yf
import datetime as dt
import plotly.graph_objs as go

# Create a Dash application
app = dash.Dash(__name__)

# Define CSS styling and heading
app.layout = html.Div([
    html.Div([
        html.Img(src="https://www.seekpng.com/png/full/15-151235_tesla-png-logo-transparent-background-tesla-logo.png", style={'width': '10%', 'float': 'left'}),
        html.Div([
            html.H2("Stock Market Data", style={'textAlign': 'center', 'color': '#007BFF'}),
            html.H3("Company:Tesla, Inc. (TSLA)", style={'textAlign': 'center', 'color': '#007BFF'}),
            html.H4(id='stock-name', style={'textAlign': 'center', 'color': '#007BFF'}),
        ], style={ 'textAlign': 'center'}),
    ]),
    dcc.Graph(id='live-graph', style={'height': '65vh'}), 
    dcc.DatePickerRange(
        id='date-range-picker',
        display_format='YYYY-MM-DD',
        start_date=dt.datetime(2020, 1, 1),  # Set your desired start date here
        end_date=dt.datetime(2023, 7, 1),    # Set your desired end date here
    ),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # 5fps
        n_intervals=0
    )
], style={'font-family': 'Arial, sans-serif', 'padding': '5px', "background-color": "#EBE6E7"})


# Define the callback for updating the graph data
def update_graph_data(start_date, end_date):
    stock_ticker = 'TSLA'  

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    try:
        data = yf.download(stock_ticker, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(f"Error downloading data: {e}")
        data = pd.DataFrame()  # Return an empty DataFrame in case of error

    return data


@app.callback([Output('live-graph', 'figure'),
               Output('stock-name', 'children')],
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('graph-update', 'n_intervals')])
def update_graph(start_date, end_date, n):
   

    data = update_graph_data(start_date, end_date)

   

    current_index = n % len(data.index)
    x_data = data.index[:current_index]
    y_data = data['Close'][:current_index]

    # Calculate the 3-month range for x-axis
    if not x_data.empty:
        one_month_ago = x_data[-1] - pd.DateOffset(months=3)
        xaxis_range = [one_month_ago, x_data[-1]]
    else:
        one_month_ago = pd.to_datetime(dt.datetime.now()) - pd.DateOffset(months=3)
        xaxis_range = [one_month_ago, dt.datetime.now()]

    trace = go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',  
        name='Stock Price',
        line={'color': 'red', 'width': 2}  
    )
    layout = go.Layout(
        title=f"Stock Data from {start_date} to {end_date}",
        xaxis=dict(title='Date', range=xaxis_range, tickfont=dict(size=12)),  # Set the x-axis 
        yaxis=dict(title='Stock Price', tickfont=dict(size=12)),  # Set the y-axis 
        margin={'l': 60, 'r': 10, 't': 80, 'b': 50}, 
        hovermode='closest',  
        hoverlabel=dict(bgcolor='#444', font_size=16, font_family='Arial', font_color='white') 
    )
    return {'data': [trace], 'layout': layout}, f"Stock: TSLA"


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
