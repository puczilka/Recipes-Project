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
    dbc.Button('Submit', color="success", id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children=''),
])

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')]
)
def on_click(n_clicks, value):

    recipe_names = recipesAPI.retrieve_data_Edamam(value)
    # Create links to external recipes' websites

    suggestions = html.Div([
        html.Br(),
        dbc.Alert("See below for suggested top recipes.", color="success"),
    ])

    nav = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(recipe_names[0][0], href=recipe_names[0][1], id="recipe"),
                    dbc.NavLink(recipe_names[0][2], href=recipe_names[0][3], id="recipe"),
                    dbc.NavLink(recipe_names[0][4], href=recipe_names[0][5], id="recipe"),
                    dbc.NavLink(recipe_names[0][6], href=recipe_names[0][7], id="recipe"),
                    dbc.NavLink(recipe_names[0][8], href=recipe_names[0][9], id="recipe")
                ]
            ),
            html.Br(),
        ]
    )

    # Display a bar chart showing nutritional value of the recipes
    app.layout = html.Div(children=[

        dcc.Graph(style={'height': '400px', "width": "1100px"},
            id='nutrition',
            figure={
                'data': [
                    {'x': ["Fat", "Sugar", "Protein", "Fiber"], 'y': [recipe_names[1][0], recipe_names[2][0], recipe_names[3][0], recipe_names[4][0]], 'type': 'bar', 'name': recipe_names[0][0]},
                    {'x': ["Fat", "Sugar", "Protein", "Fiber"], 'y': [recipe_names[1][1], recipe_names[2][1], recipe_names[3][1], recipe_names[4][1]], 'type': 'bar', 'name': recipe_names[0][2]},
                    {'x': ["Fat", "Sugar", "Protein", "Fiber"], 'y': [recipe_names[1][2], recipe_names[2][2], recipe_names[3][2], recipe_names[4][2]], 'type': 'bar', 'name': recipe_names[0][4]},
                    {'x': ["Fat", "Sugar", "Protein", "Fiber"], 'y': [recipe_names[1][3], recipe_names[2][3], recipe_names[3][3], recipe_names[4][3]], 'type': 'bar', 'name': recipe_names[0][6]},
                    {'x': ["Fat", "Sugar", "Protein", "Fiber"], 'y': [recipe_names[1][4], recipe_names[2][4], recipe_names[3][4], recipe_names[4][4]], 'type': 'bar', 'name': recipe_names[0][8]},
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

    return suggestions, nav, app.layout


if __name__ == '__main__':
    app.run_server(debug=True)