import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Read the avocado dataset
df = pd.read_csv('avocado.csv')

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the app with CSS styling
app.layout = html.Div([
    html.H1("Avocado Dataset Visualization", style={'color': '#0066CC', 'text-align': 'center', 'padding-top': '20px', 'font-size': '34px'}),
    
    html.Div([
        html.Label("Filter by Time:", style={'color': '#6600CC', 'font-size': '24px'}),
        dcc.Dropdown(
            id='time-filter',
            options=[{'label': year, 'value': year} for year in df['year'].unique()],
            multi=True,
            value=[2017]  
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Label("Filter by Region:", style={'color': '#6600CC', 'font-size': '24px'}),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': region, 'value': region} for region in df['region'].unique()],
            multi=True,
            value=['Albany'] 
        )
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Label("Filter by Type:", style={'color': '#6600CC', 'font-size': '24px'}),
        dcc.Dropdown(
            id='type-filter',
            options=[{'label': avocado_type, 'value': avocado_type} for avocado_type in df['type'].unique()],
            multi=True,
            value=['organic'] 
        )
    ], style={'margin': '20px'}),
    
    dcc.Graph(
        id='bar-chart',
        config={
            'displayModeBar': False  
        },
        style={'margin': '20px'}
    )
], style={'background-color': '#f2f2f2', 'padding': '20px'})

# Define the callback for updating the bar chart based on filters
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('time-filter', 'value'),
     Input('region-filter', 'value'),
     Input('type-filter', 'value')]
)
def update_bar_chart(selected_years, selected_regions, selected_types):
    filtered_df = df[
        (df['year'].isin(selected_years)) &
        (df['region'].isin(selected_regions)) &
        (df['type'].isin(selected_types))
    ]
    fig = px.bar(
        filtered_df,
        x='Date',
        y='AveragePrice',
        color='Total Bags',
        hover_data=['region', 'type'],
        title='Avocado Prices and Volume'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
