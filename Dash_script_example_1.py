import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import numpy as np

# x = np.arange(10)
# fig = go.Figure(data=go.Scatter(x=x, y=np.sin(x)))

# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=np.arange(0, 10, 0.01),
            y=np.sin(step * np.arange(0, 10, 0.01))))

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

my_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# my_app = dash.Dash('')

my_app.layout = html.Div([
    html.H1(
        children="Very cool sin curve ediy"),
    dcc.Graph(figure=fig)
])

# my_app.server.run(debug=True)

if __name__ == '__main__':
    my_app.run_server(debug=True)
