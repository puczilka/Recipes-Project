import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import json
import testapi

# Initialise Dash app

app = dash.Dash(__name__, external_stylesheets=[
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
], external_scripts=[
    'https://code.jquery.com/jquery-3.3.1.slim.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js'
])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Recipe',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Web-based app for panic buying and food waste prevention during COVID-19 lock down', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div([
        html.Label('Insert your ingredients to find your perfect recipe!'),
        dcc.Input(id='input-on-submit', type='text'),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
             children='Enter a value and press submit')])])

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])

def retrieve_recipes(n_clicks, value):
    food = testapi.retrieve_data(value)
    nav = html.Div(
    [
        dbc.Nav([

        dbc.NavLink(food[0][0], href= food[1][0]),
        dbc.NavLink(food[0][1], href= food[1][1]),
        dbc.NavLink(food[0][2], href= food[1][2]),
        dbc.NavLink(food[0][3], href= food[1][3]),
        dbc.NavLink(food[0][4], href= food[1][4]),])


        ,
        html.Br(),
    ]
    )
    return nav

if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False,dev_tools_props_check=False)