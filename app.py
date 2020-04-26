import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import spoonacularapi
import plotly.graph_objs as go

app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Alert("Type in the ingredients and we will suggest recipes!", color="success"),
    html.Div(dcc.Input(id='input-on-submit', placeholder="Type in your ingredients separated by coma...",  type='text', style={'width': '30%'})),
    dbc.Button('Submit', color="success", id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children=''),
    dbc.FormGroup(
        [
            dbc.Label("Choose one off recipe, or Meal plan"),
            dbc.Checklist(
                options=[
                    {"label": "Meal plan", "value": 1},
                ],
                value=[],
                id="switches-input",
                switch=True,
            ),
        ]
    ),
    dbc.FormGroup([
        dbc.Label("Choose dietary preferences"),
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
        dbc.Label("Choose Cuisines to exclude"),
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
            ],
            value=[],
            id="checklist-input-cuisine",
            inline= True
        ),
    ])
    #"african, american, british, cajun, caribbean, chinese, eastern european, european, french,
    # " \"german, greek, indian, irish, italian, japanese, jewish, korean, latin american, mediterranean,
    # " \"mexican, middle eastern, nordic, southern, spanish, thai, vietnamese"

])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks'),
     dash.dependencies.Input("checklist-input-diet", "value"),
     dash.dependencies.Input("checklist-input-cuisine", "value"),
     dash.dependencies.Input("switches-input", "value")],
    [dash.dependencies.State('input-on-submit', 'value')]

)



def on_click(n_clicks, diet_value, cuisine_value, meal_plan,  value  ):
    print("hello world", diet_value,cuisine_value, meal_plan)
    cuisine_total, diet_out= spoonacularapi.filters(cuisine_value, diet_value)

    if len(meal_plan)>= 1:  # then the switch box is switched
        recipe_return_value=100 #meal plan requires maximum number of recipes to be filtered
    else:
        recipe_return_value=5   # normal operation requires top 5 recipes

    ingredients_tot, recipe_names, id_array, source_url, image=spoonacularapi.get_recipes(cuisine_total, diet_out, value, recipe_return_value)
    #recipe_names = spoonacularapi.retrieve_data(value)
    recipe_names= spoonacularapi.get_name_url_nutrients(id_array, recipe_names, source_url, image,  value)

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

# Display images of the meals
    app.images = html.Div(children=[ html.Img(src=recipe_names[2][0]),
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

    return suggestions, nav, app.images, app.bar_chart, app.horizontal_bar_chart


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
