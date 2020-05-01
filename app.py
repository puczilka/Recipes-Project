import os
from random import randint
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import spoonacularapi
import plotly.graph_objs as go
import flask
from dash.dependencies import Input, Output


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

app.config.suppress_callback_exceptions = True

# This shows the location of the name page
url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app_layout = html.Div([
    dbc.Jumbotron(
        [
            dbc.Container(
                [
                    html.H1("Welcome to PlanIt Food ", className="display-3", style={'color': 'white', 'fontSize': 50}),
                    html.P(
                        "Reduce waste, save time and PlanIt",
                        className="lead", id="check-list", style={'color': 'white', 'fontSize': 25}
                    ),
                    html.Br(),

                    html.P(
                        "Type in your main ingredients to get recipe ideas",
                        className="lead",style={'color': 'white', 'fontSize': 20},
                    ),

                    html.P(
                        "OR",
                        className="lead",style={'color': 'white', 'fontSize': 20},
                    ),

                    # Hyperlink to /meal-planning which opens in a new tab
                    dcc.Link('Click here to go to Meal Planning', href='/meal-planning', target="blank", id="navigate", style={'color': 'white', 'fontSize': 20})
                ],
                id="jumbotron",
                style={'backgroundImage': 'url(https://images.pexels.com/photos/1565982/pexels-photo-1565982.jpeg)', 'background-size': '100%','backgroundRepeat': 'no-repeat', 'backgroundPosition': 'left', 'backgroundSize': 'cover'},#, 'position': 'fixed'},
                fluid=True,
            )
        ],
        fluid=True,
        id="jumbotronBox",
    ),

    dbc.Alert("Type in your ingredients and select preferences.", color="success", id="check-list"),

    dbc.FormGroup([
        dbc.Label("Choose Dietary Preferences", id="check-list"),
        dbc.Checklist(
            options=[
                {"label": "Vegan", "value": 1},
                {"label": "Vegetarian", "value": 2},
                {"label": "Pescetarian", "value": 3},
                {"label": "Gluten Free", "value": 4},
                {"label": "Ketogenic", "value": 5},
            ],
            value=[],
            id="checklist-input-diet",
        ),
    ]),

    dbc.FormGroup([
        dbc.Label("Choose cuisines to exclude", id="check-list"),
        dbc.Checklist(
            options=[
                {"label": "African", "value": 1},
                {"label": "American", "value": 2},
                {"label": "British", "value": 3},
                {"label": "Cajun", "value": 4},
                {"label": "Caribbean", "value": 5},
                {"label": "Chinese", "value": 6},
                {"label": "Eastern European", "value": 7},
                {"label": "French", "value": 8},
                {"label": "German", "value": 9},
                {"label": "Greek", "value": 10},
                {"label": "Indian", "value": 11},
                {"label": "Irish", "value": 12},
                {"label": "Italian", "value": 13},
                {"label": "Japanese", "value": 14},
                {"label": "Jewish", "value": 15},
                {"label": "Korean", "value": 16},
                {"label": "Latin American", "value": 17},
                {"label": "Mediterranean", "value": 18},
                {"label": "Mexican", "value": 19},
                {"label": "Middle Eastern", "value": 20},
                {"label": "Nordic", "value": 21},
                {"label": "Southern", "value": 22},
                {"label": "Spanish", "value": 23},
                {"label": "Thai", "value": 24},
                {"label": "Vietnamese", "value": 25},
                # "african, american, british, cajun, caribbean, chinese, eastern european, european, french,
                # " \"german, greek, indian, irish, italian, japanese, jewish, korean, latin american, mediterranean,
                # " \"mexican, middle eastern, nordic, southern, spanish, thai, vietnamese"
            ],
            value=[],
            id="checklist-input-cuisine",
            inline=True
        ),
        html.Br(),

        html.Div(
            dcc.Input(id='input-on-submit1', placeholder="Type in your ingredients separated by comma...", type='text',
                      style={'width': '30%'})),
        dbc.Button('Submit', color="success", id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic', children=''),
    ])
])
layout_meal_planning = html.Div([
    dbc.Jumbotron(
        [
            dbc.Container(
                [
                    html.H1("Meal Planning Tool", className="display-3", style={'color': 'white', 'fontSize': 50}),
                    html.P(
                        "Reduce waste, save time and PlanIt ",
                        className="lead", id="check-list", style={'color': 'white', 'fontSize': 30}
                    ),
                    html.Br(),
                    html.P(
                        "Generate your meal plan by typing in at least 10 ingredients",
                        className="lead", style={'color': 'white', 'fontSize': 20},
                    ),

                    dcc.Link('Click here to go back', href='/', target="blank", style={'color': 'white', 'fontSize': 18}),
                ],
                id="jumbotron",
                style={'backgroundImage': 'url(https://images.pexels.com/photos/1565982/pexels-photo-1565982.jpeg)', 'background-size': '100%', 'backgroundRepeat': 'no-repeat', 'backgroundPosition': 'left', 'backgroundSize': 'cover'},#, 'position': 'fixed'},
                fluid=True,
            )
        ],
        fluid=True,
        id="jumbotronBox",
    ),

    dbc.Alert("Type in 10 (or more) ingredients to generate a Meal Plan!", color="success", id="check-list"),

    html.Br(),

    dbc.FormGroup([
        dbc.Label("Choose Dietary Preferences"),
        dbc.Checklist(
            options=[
                {"label": "Vegan", "value": 1},
                {"label": "Vegetarian", "value": 2},
                {"label": "Pescetarian", "value": 3},
                {"label": "Gluten Free", "value": 4},
                {"label": "Ketogenic", "value": 5},
            ],
            value=[],
            id="checklist-input-diet2",
        ),
    ]),

    dbc.FormGroup([
        dbc.Label("Choose cuisines to exclude"),
        dbc.Checklist(
            options=[
                {"label": "African", "value": 1},
                {"label": "American", "value": 2},
                {"label": "British", "value": 3},
                {"label": "Cajun", "value": 4},
                {"label": "Caribbean", "value": 5},
                {"label": "Chinese", "value": 6},
                {"label": "Eastern European", "value": 7},
                {"label": "French", "value": 8},
                {"label": "German", "value": 9},
                {"label": "Greek", "value": 10},
                {"label": "Indian", "value": 11},
                {"label": "Irish", "value": 12},
                {"label": "Italian", "value": 13},
                {"label": "Japanese", "value": 14},
                {"label": "Jewish", "value": 15},
                {"label": "Korean", "value": 16},
                {"label": "Latin American", "value": 17},
                {"label": "Mediterranean", "value": 18},
                {"label": "Mexican", "value": 19},
                {"label": "Middle Eastern", "value": 20},
                {"label": "Nordic", "value": 21},
                {"label": "Southern", "value": 22},
                {"label": "Spanish", "value": 23},
                {"label": "Thai", "value": 24},
                {"label": "Vietnamese", "value": 25},
                # "african, american, british, cajun, caribbean, chinese, eastern european, european, french,
                # " \"german, greek, indian, irish, italian, japanese, jewish, korean, latin american, mediterranean,
                # " \"mexican, middle eastern, nordic, southern, spanish, thai, vietnamese"
            ],
            value=[],
            id="checklist-input-cuisine2",
            inline=True
        ),
        html.Br(),
        html.Div(
            dcc.Input(id='input-on-submit2', placeholder="Type in your ingredients separated by comma...", type='text',
                      style={'width': '30%'})),

        dbc.Button('Submit', color="success", id='submit-val2', n_clicks=0),
        html.Div(id='container-button-meal-plan', children=''),

        html.Br(),
        dcc.Link('Go back', href='/', target="blank"),
    ])
])

# Layout of the /meal-planning page


def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        app_layout,
        layout_meal_planning,
    ])


app.layout = serve_layout


# Determines which page gets displayed by checking the "pathname"
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/meal-planning":
        return layout_meal_planning
    else:
        return app_layout


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks'),
     dash.dependencies.Input("checklist-input-diet", "value"),
     dash.dependencies.Input("checklist-input-cuisine", "value")],
    [dash.dependencies.State('input-on-submit1', 'value')]
)
def on_submit_click(n_clicks, diet_value, cuisine_value, value):
    # print("hello world", diet_value, cuisine_value, value)# meal_plan)

    # Added because otherwise a random recipe was displayed on the website BEFORE submit button was pressed
    if value == None:
        return

    cuisine_total, diet_out = spoonacularapi.filters(cuisine_value, diet_value)

    # if len(meal_plan)>= 1:  # then the switch box is switched
    #     recipe_return_value = 100   # meal plan requires maximum number of recipes to be filtered
    # else:
    recipe_return_value = 5   # normal operation requires top 5 recipes

    ingredients_tot, recipe_names, id_array, source_url, image = spoonacularapi.get_recipes(cuisine_total, diet_out, value, recipe_return_value)

    # recipe_names = spoonacularapi.retrieve_data(value)
    recipe_names = spoonacularapi.get_name_url_nutrients(id_array, recipe_names, source_url, image, value)

    suggestions = html.Div([
        html.Br(),
        dbc.Alert("See below for the best matches.", color="success", id="check-list"),
    ])

    if len(recipe_names[0]) >= 4:
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

        # Display images of the meals
        app.images = html.Div(children=[html.Img(src=recipe_names[2][0]),
                                         html.Img(src=recipe_names[2][1]),
                                         html.Img(src=recipe_names[2][2]),
                                         html.Img(src=recipe_names[2][3]),
                                         html.Img(src=recipe_names[2][4])])

        # Display a bar chart showing nutritional value of the recipes
        app.bar_chart = html.Div(children=[
            dcc.Graph(style={'height': '400px', "width": "1100px"},
                id='bar_chart',
                figure={
                    'data': [
                        {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[3][0], recipe_names[4][0], recipe_names[5][0]], 'type': 'bar', 'name': recipe_names[0][0]},
                        {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[3][1], recipe_names[4][1], recipe_names[5][1]], 'type': 'bar', 'name': recipe_names[0][1]},
                        {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[3][2], recipe_names[4][2], recipe_names[5][2]], 'type': 'bar', 'name': recipe_names[0][2]},
                        {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[3][3], recipe_names[4][3], recipe_names[5][3]], 'type': 'bar', 'name': recipe_names[0][3]},
                        {'x': ["Fat", "Carbohydrates", "Protein"], 'y': [recipe_names[3][4], recipe_names[4][4], recipe_names[5][4]], 'type': 'bar', 'name': recipe_names[0][4]},
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
                          'data': [go.Bar(x=[recipe_names[6][0], recipe_names[6][1], recipe_names[6][2], recipe_names[6][3], recipe_names[6][4]],
                                          y=[recipe_names[0][0], recipe_names[0][1], recipe_names[0][2], recipe_names[0][3], recipe_names[0][4]],
                                          orientation='h')],
                          'layout': go.Layout(
                              height=350,
                              width=1100,
                              xaxis_title="Calories (kcal)",
                              title="Calories comparison between recipes",
                              margin=dict(
                                  l=350,
                                  t=50,
                              ),
                          ),
                      }
                    )
        ])
    else:
        return dbc.Alert("Try typing in different ingredients as no results have been found.", color="warning", id="check-list")

    return suggestions, nav, app.images, app.bar_chart, app.horizontal_bar_chart


@app.callback(
    dash.dependencies.Output('container-button-meal-plan', 'children'),
    [dash.dependencies.Input('submit-val2', 'n_clicks'),
     dash.dependencies.Input("checklist-input-diet2", "value"),
     dash.dependencies.Input("checklist-input-cuisine2", "value")],
    [dash.dependencies.State('input-on-submit2', 'value')]
)
def on_click(n_clicks, diet_value, cuisine_value, value):
    # print("hello world", diet_value,cuisine_value)#, meal_plan)

    # Added because otherwise a random recipe was displayed on the website BEFORE submit button was pressed
    if value == None:
        return

    cuisine_total, diet_out= spoonacularapi.filters(cuisine_value, diet_value)
    # print(cuisine_total, diet_out, value, "inputs to api")
    # if len(meal_plan)>= 1:  # then the switch box is switched
    #     recipe_return_value = 100   # meal plan requires maximum number of recipes to be filtered
    # else:
    recipe_return_value = 5   # normal operation requires top 5 recipes

    ingredients_tot, recipe_names, id_array, source_url, image = spoonacularapi.get_recipes(cuisine_total, diet_out,
                                                                                            value, recipe_return_value)

    # recipe_names = spoonacularapi.retrieve_data(value)
    recipe_names = spoonacularapi.get_name_url_nutrients(id_array, recipe_names, source_url, image, value)

    suggestions = html.Div([
        html.Br(),

        dbc.Alert("See below for the best matches", color="success", id="check-list"),
    ])

    if len(recipe_names[0]) >= 4:
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

        # Display images of the meals
        app.images = html.Div(children=[ html.Img(src=recipe_names[2][0]),
                                         html.Img(src=recipe_names[2][1]),
                                         html.Img(src=recipe_names[2][2]),
                                         html.Img(src=recipe_names[2][3]),
                                         html.Img(src=recipe_names[2][4])])

        radioitems = dbc.FormGroup(
            [
                html.Br(),
                dbc.Alert("Choose one recipe", color="success", id="check-list"),
                dbc.RadioItems(
                    options=[
                        {"label": '"' + recipe_names[0][0]+'"' + " uses the ingredients: " + ', '.join(ingredients_tot[0]), "value": ingredients_tot[0]},
                        {"label": '"' + recipe_names[0][1]+'"' + " uses the ingredients: " + ', '.join(ingredients_tot[1]), "value": ingredients_tot[1]},
                        {"label": '"' + recipe_names[0][2]+'"' + " uses the ingredients: " + ', '.join(ingredients_tot[2]), "value": ingredients_tot[2]},
                        {"label": '"' + recipe_names[0][3]+'"' + " uses the ingredients: " + ', '.join(ingredients_tot[3]), "value": ingredients_tot[3]},
                        {"label": '"' + recipe_names[0][4]+'"' + " uses the ingredients: " + ', '.join(ingredients_tot[4]), "value": ingredients_tot[4]},
                    ],
                    value=[],
                    id="radioitems-choice-1",
                ),
            ]
        )
        html.Br(),

        button = html.Div(
            [
                dbc.Button("Decision made!", id="example-button", color="success", className="mr-2"),
                html.Div(id='container-button-basic', children=''),
            ]
        )
        html.Br(),

    else:
        return dbc.Alert("Try typing in different ingredients as no results have been found.", color="warning", id="check-list")

    return suggestions, nav, app.images, radioitems, button


@app.callback(
    dash.dependencies.Output("container-button-basic", "children"),
    [
        dash.dependencies.Input("radioitems-choice-1", "value"),
        dash.dependencies.Input("checklist-input-diet2", "value"),
        dash.dependencies.Input("checklist-input-cuisine2", "value")
    ],
    [dash.dependencies.State('input-on-submit2', 'value')]
)
def on_meal_planning_click(choice, diet_value, cuisine_value, value):
    # print(choice, type(choice), value)

    # Added because otherwise a random recipe was displayed on the website BEFORE submit button was pressed
    if value == None:
        return

    unused_ingred = spoonacularapi.unused_ingr(value, choice)
    unused = ', '.join(unused_ingred)
    cuisine_total, diet_out = spoonacularapi.filters(cuisine_value, diet_value)

    recipe_return_value = 5  # normal operation requires top 5 recipes

    ingredients_tot, recipe_names, id_array, source_url, image = spoonacularapi.get_recipes(cuisine_total, diet_out,
                                                                                            unused, recipe_return_value)

    recipe_names = spoonacularapi.get_name_url_nutrients(id_array, recipe_names, source_url, image, value)

    suggestions2 = html.Div([
        html.Br(),
        dbc.Alert("See below for the best matches using the remaining ingredients: " + unused, color="success"),
    ])

    nav2 = html.Div(
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

    # Display images of the meals
    app.images2 = html.Div(children=[html.Img(src=recipe_names[2][0]),
                                    html.Img(src=recipe_names[2][1]),
                                    html.Img(src=recipe_names[2][2]),
                                    html.Img(src=recipe_names[2][3]),
                                    html.Img(src=recipe_names[2][4])])

    return suggestions2, nav2, app.images2


if __name__ == '__main__':
    app.server.run(threaded=True, debug=False)
