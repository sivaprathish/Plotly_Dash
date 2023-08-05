import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data 
df = pd.read_csv('countries.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundImage': "url('https://www.researchgate.net/profile/Houssain-Kettani/publication/268290952/figure/fig2/AS:669504350720006@1536633684765/A-color-coded-map-of-the-World-illustrating-the-presence-of-Muslims-in-each-country-the.ppm')",
    'backgroundSize': 'cover',
    'backdropFilter': 'blur(5px)'
   
}, children=[
    html.Div(className="content", children=[
        html.H1("World Population by Country"),
        
        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': column, 'value': column} for column in df.columns],
            value=df.columns[0]
        ),
        
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': column, 'value': column} for column in df.columns],
            value='pop1980'
        ),
        
        dcc.Dropdown(
            id='top-dropdown',
            options=[{'label': f"Top {i}", 'value': i} for i in [5, 10,20,30,50,100]],
            value=5
        ),
        
        dcc.Graph(id='country-graph',),
    ])
])

# Callback to update the graph 
@app.callback(
    Output('country-graph', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('top-dropdown', 'value')]
)
def update_graph(x_axis, y_axis, top_n):
    sorted_df = df.sort_values(by=y_axis, ascending=False).head(top_n)
    fig = px.bar(sorted_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis} (Top {top_n})",
                 hover_data=[x_axis, y_axis])  # Add hover_data to show x and y values
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
