import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np

# Generate random data for the heatmap
np.random.seed(0)
data = np.random.rand(40, 160)

# Define the layout of the app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='heatmap'),
    dcc.Interval(id='interval', interval=200, n_intervals=0, max_intervals=-1)
])

# Define the callback to update the heatmap
@app.callback(Output('heatmap', 'figure'), Input('interval', 'n_intervals'))
def update_heatmap(n):
    # Generate random data for the heatmap
    data = np.random.rand(40, 160)
    return go.Figure(
        data=go.Heatmap(z=data),
        layout=go.Layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=0, r=0, t=0, b=0)
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)