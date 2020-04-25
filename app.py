import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import spoonacularapi
import plotly.graph_objs as go

app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Alert("Type in the ingredients and we will suggest recipes!", color="success"),
    html.Div(dcc.Input(id='input-on-submit', placeholder="Type in ingredients...",  type='text')),
    dbc.Button('Submit', color="success", id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children=''),
])

print("Hellooooo")
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')]
)
def on_click(n_clicks, value):

    recipe_names = spoonacularapi.retrieve_data(value)

    suggestions = html.Div([
        html.Br(),
        dbc.Alert("See below for the best matches.", color="success"),
    ])

    nav = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(recipe_names[0][0], href=recipe_names[1][0], id="recipe"),
                    dbc.NavLink(recipe_names[0][1], href=recipe_names[1][1], id="recipe"),
                    dbc.NavLink(recipe_names[0][2], href=recipe_names[1][2], id="recipe"),
                    dbc.NavLink(recipe_names[0][3], href=recipe_names[1][3], id="recipe"),
                    dbc.NavLink(recipe_names[0][4], href=recipe_names[1][4], id="recipe")
                ]
            ),
            html.Br(),
        ]
    )

    # Display a bar chart showing nutritional value of the recipes
    app.bar_chart = html.Div(children=[

        dcc.Graph(style={'height': '400px', "width": "1100px"},
            id='bar_chart',
            figure={
                'data': [
                    {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[2][0], recipe_names[3][0], recipe_names[4][0]], 'type': 'bar', 'name': recipe_names[0][0]},
                    {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[2][1], recipe_names[3][1], recipe_names[4][1]], 'type': 'bar', 'name': recipe_names[0][1]},
                    {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[2][2], recipe_names[3][2], recipe_names[4][2]], 'type': 'bar', 'name': recipe_names[0][2]},
                    {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[2][3], recipe_names[3][3], recipe_names[4][3]], 'type': 'bar', 'name': recipe_names[0][3]},
                    {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[2][4], recipe_names[3][4], recipe_names[4][4]], 'type': 'bar', 'name': recipe_names[0][4]},
                ],
                'layout': go.Layout(
                    height=350,
                    width=1100,
                    yaxis_title="Amount (g)",
                    title="Comparison of nutritional values between the recipes",
                    margin=dict(
                        b=50,
                        r=50,
                    ),
                )
            }
        )
    ])

    # Display a horizontal bar chart showing calories
    app.horizontal_bar_chart = html.Div([
        dcc.Graph(
                  id='horizontal_bar_chart',
                  figure={
                      'data': [go.Bar(x=[recipe_names[5][0], recipe_names[5][1], recipe_names[5][2], recipe_names[5][3], recipe_names[5][4]],
                                      y=[recipe_names[0][0], recipe_names[0][1], recipe_names[0][2], recipe_names[0][3], recipe_names[0][4]],
                                      orientation='h')],
                      'layout': go.Layout(
                          height=350,
                          width=1100,
                          xaxis_title="Calories (kcal)",
                          title="Calories comparison between recipes",
                          margin=dict(
                              l=300,
                              t=50,
                          ),
                      ),
                  }
                )
    ])

    return suggestions, nav, app.bar_chart, app.horizontal_bar_chart


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
