import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import numpy as np

N = 100
a_1 = 100
a_2 = 100

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
height = 1000

app.layout = html.Div([
    dcc.Graph(
        id='graph-with-slider',
        style={
            'margin': '0 auto',
            'height': '{}px'.format(str(height)),
            'width': '{}px'.format(str(height))
        }
    ),
    html.Div(
        id='output-container-range-sliders',
        style={
                'textAlign': 'center'
        }
    ),
    html.Br(),
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='z_radio_item',
                options=[{'label': i, 'value': i} for i in ['pizza', 'christmas-pudding', 'doughnut', 'half-bagel']],
                value='pizza',
                labelStyle={'display': 'inline-block'}
            )],
            style={
                'textAlign': 'center'
            }
        ),
        html.Br(),
        dcc.Slider(
            id='a1_slider',
            min=0,
            max=a_1,
            value=a_1 / 2,
            marks={str(0): str(0), str(a_1): str(a_1)}
        ),
        dcc.Slider(
            id='a2_slider',
            min=0,
            max=a_2,
            value=a_2 / 2,
            marks={str(0): str(0), str(a_2): str(a_2)}
        ),
        dcc.Slider(
            id='N_slider',
            min=0,
            max=N,
            value=N / 2,
            marks={str(0): str(0), str(a_2): str(a_2)}
        ),
        # html.Br(),
        html.Div([
            dcc.RadioItems(
                id='line-mode',
                options=[{'label': i, 'value': i} for i in ['lines', 'markers']],
                value='lines',
                labelStyle={'display': 'inline-block'}
            )],
            style={
                'textAlign': 'center'
            })
    ], style={
        'margin': '0 auto',
        'width': '{}px'.format(str(height - 130))
    }),
    html.Br()
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('a1_slider', 'value'),
     Input('a2_slider', 'value'),
     Input('N_slider', 'value'),
     Input('z_radio_item', 'value'),
     Input('line-mode', 'value')])
def update_figure(selected_a1, selected_a2, selected_N, selected_z, selected_mode):

    sum = selected_a1 + selected_a2

    updated_ratio = (selected_a1 + selected_a2) / selected_a2
    beta = np.linspace(0, 2 * np.pi, 10000)  # could multiply step by a factor of selected_N

    x, y = selected_a1 * np.cos(selected_N * beta) + selected_a2 * np.cos(updated_ratio * selected_N * beta), \
           selected_a1 * np.sin(selected_N * beta) + selected_a2 * np.sin(updated_ratio * selected_N * beta)

    if selected_z == 'pizza':
        z = 0 * beta
    if selected_z == 'christmas-pudding':
        z = np.sqrt(sum ** 2 - (x ** 2 + y ** 2))
    elif selected_z == 'doughnut':
        z = -selected_a2 * np.sin((1 - updated_ratio) * selected_N * beta)

    elif selected_z == 'half-bagel':
        z = np.abs(-selected_a2 * np.sin((1 - updated_ratio) * selected_N * beta))

    fig = go.Figure(data=go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode=selected_mode,
        line=dict(
            width=5,
            color='darkblue'
        ),
        marker=dict(
            size=2,
            color=z,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            # opacity=0.8
            opacity=1
        )
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, tickwidth=2, range=[-sum, sum], ),
            yaxis=dict(nticks=4, tickwidth=2, range=[-sum, sum], ),
            zaxis=dict(nticks=4, tickwidth=2, range=[-sum, sum], ), ),
        # width=height,
        scene_aspectmode='cube'
    )
    return fig


@app.callback(
    Output('output-container-range-sliders', 'children'),
    [Input('a1_slider', 'value'),
     Input('a2_slider', 'value'),
     Input('N_slider', 'value')])
def slider_value(a1_value, a2_value, N_value):
    return "a_1 = " + str(a1_value) + "....a_2 = " + str(a2_value) + "....N = " + str(N_value)


if __name__ == '__main__':
    app.run_server(debug=True)
