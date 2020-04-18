import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import recipesAPI

app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dbc.Alert("Type in the ingredients and we will suggest recipes!", color="success"),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')]
)
def on_click(n_clicks, value):

    recipe_names = recipesAPI.retrieve_data_Edamam(value)

    # Create links to external recipes' websites
    nav = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(recipe_names[0][0], href=recipe_names[0][1]),
                    dbc.NavLink(recipe_names[0][2], href=recipe_names[0][3]),
                    dbc.NavLink(recipe_names[0][4], href=recipe_names[0][5]),
                ]
            ),
            html.Br(),
        ]
    )

    # Display a bar chart showing nutritional value of the recipes
    app.layout = html.Div(children=[

        dcc.Graph(
            id='nutrition',
            figure={
                'data': [
                    {'x': ["Fat", "Sugar"], 'y': [recipe_names[1][0], recipe_names[2][0]], 'type': 'bar', 'name': recipe_names[0][0]},
                    {'x': ["Fat", "Sugar"], 'y': [recipe_names[1][1], recipe_names[2][1]], 'type': 'bar', 'name': recipe_names[0][2]},
                    {'x': ["Fat", "Sugar"], 'y': [recipe_names[1][2], recipe_names[2][2]], 'type': 'bar', 'name': recipe_names[0][4]},
                ],
                'layout': {
                    'title': 'Comparision of nutritional values between the recipes',
                    'yaxis': {
                        'title': 'Amount (g)'
                    }
                }
            }
        )
    ])

    return nav, app.layout


if __name__ == '__main__':
    app.run_server(debug=True)