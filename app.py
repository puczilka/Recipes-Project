import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import recipesAPI

app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    html.A("Link to external site", href='https://plot.ly', target="_blank")
])


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

    nav = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(recipe_names[0], href=recipe_names[1]),
                    dbc.NavLink(recipe_names[2], href=recipe_names[3]),
                    dbc.NavLink(recipe_names[4], href=recipe_names[5]),
                ]
            ),
            html.Br(),
        ]
    )


    return nav



if __name__ == '__main__':
    app.run_server(debug=True)