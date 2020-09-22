
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import numpy as np

N = 100
a_1 = 100
a_2 = 100

# ratio = (a_1 + a_2) / a_2
#
# x, y = a_1 * np.cos(N * beta) + a_2 * np.cos(ratio * N * beta), \
#        a_1 * np.sin(N * beta) + a_2 * np.sin(ratio * N * beta)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
height = 600
app.layout = html.Div([
    dcc.Graph(
        id='graph-with-slider',
        style={
            'margin': '0 auto',
            'height': '{}px'.format(str(height)),
            'width': '{}px'.format(str(height-20))
        }
    ),
    html.Div([
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
        )
    ], style={
        'margin': '0 auto',
        'width': '{}px'.format(str(height-130))
    })
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('a1_slider', 'value'),
     Input('a2_slider', 'value'),
     Input('N_slider', 'value')])
def update_figure(selected_a1, selected_a2, selected_N):
    sum = selected_a1 + selected_a2
    updated_ratio = (selected_a1 + selected_a2) / selected_a2
    beta = np.linspace(0, 2 * np.pi, 10000)

    x, y = selected_a1 * np.cos(selected_N * beta) + selected_a2 * np.cos(updated_ratio * selected_N * beta), \
           selected_a1 * np.sin(selected_N * beta) + selected_a2 * np.sin(updated_ratio * selected_N * beta)

    layout = go.Layout(yaxis=dict(range=[-sum, sum]),
                       xaxis=dict(range=[-sum, sum]))

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'),
                    layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
