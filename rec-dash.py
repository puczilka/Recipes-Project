import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()
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

    html.Label('Insert your ingredients to find your perfect recipe!'),
    dcc.Input(value='Insert Ingredients', type='text')
])



if __name__ == '__main__':
    app.run_server(debug=True)