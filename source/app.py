import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import time

# create a list of 2D arrays with random data for the heatmaps
heatmap_data = [np.random.randint(10, size=(40, 40)) for i in range(60)]

# set up the Dash app
app = dash.Dash(__name__)

# create the layout for the app
app.layout = html.Div([
    # add the heatmap plot
    dcc.Graph(id='heatmap'),
    # add a slider to control the animation
    dcc.Slider(id='heatmap-slider', min=0, max=len(heatmap_data)-1, value=0, marks={str(i): str(i) for i in range(len(heatmap_data))}),
    # add a button for pausing and unpausing the animation
    html.Button(id='animate-button', children='Pause', n_clicks=0),
], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

# create a callback function to update the heatmap plot using an animation
@app.callback(
    dash.dependencies.Output('heatmap', 'figure'),
    [dash.dependencies.Input('heatmap-slider', 'value'),
     dash.dependencies.Input('animate-button', 'n_clicks')])
def update_heatmap(slider_value, n_clicks):
    # create the heatmap trace
    heatmap_trace = go.Heatmap(z=heatmap_data[0], zmin=0, zmax=9, colorscale='Viridis')
    # create the scatter trace to show the current frame
    scatter_trace = go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='red', size=10))
    # create the figure
    fig = go.Figure(data=[heatmap_trace, scatter_trace])
    fig.update_layout(title='Heatmap', xaxis_title='X Axis', yaxis_title='Y Axis', width=600, height=600)
    fig.update_layout(updatemenus=[dict(type='buttons',
                                        showactive=False,
                                        buttons=[dict(label='Play',
                                                      method='animate',
                                                      args=[None, {'frame': {'duration': 50, 'redraw': True},
                                                                   'fromcurrent': True,
                                                                   'transition': {'duration': 0}}]),
                                                 dict(label='Pause',
                                                      method='animate',
                                                      args=[[None], {'frame': {'duration': 0, 'redraw': False},
                                                                     'mode': 'immediate',
                                                                     'transition': {'duration': 0}}])])])
    # add the frames to the animation
    frames = [dict(data=[dict(z=heatmap_data[i]), dict(x=[i % 40], y=[i // 40])]) for i in range(len(heatmap_data))]
    fig.frames = frames
    
    # determine the current frame based on the slider value
    current_frame = slider_value
    fig.update(frames=[dict(name=i) for i in range(len(heatmap_data))])
    fig.update_layout(transition={'duration': 0})
    fig['layout']['sliders'][0]['active'] = current_frame
    fig.data[1]['x'] = [current_frame % 40]
    fig.data[1]['y'] = [current_frame // 40]
    return fig

if __name__ == '__main__':
    # start the app server
    app.run_server(debug=True)
