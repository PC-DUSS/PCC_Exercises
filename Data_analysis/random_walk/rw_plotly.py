"""
Pierre-Charles Dussault
March 17, 2021.

Generate random coordinates, representing a 'random walk'. Visualize the path
taken during this walk with the plotly Python library.
"""
import plotly.graph_objs as go
from plotly import offline
from random_walk import RandomWalk


def main():

    my_random_walk = RandomWalk()
    my_random_walk.fill_walk()
    point_number = list(range(my_random_walk.num_points))
    data = [{
        'type': 'scatter',
        'mode': 'markers',
        'x': my_random_walk.x_values,
        'y': my_random_walk.y_values,
        'marker': {
            'size': 6,
            'color': point_number,
            'colorscale': 'tealgrn',
            'colorbar': {
                'title': 'Progress (steps taken)',
                }
            }
        }]
    my_layout = go.Layout(title='A Random Walk')
    fig_dict = {'data': data, 'layout': my_layout}
    offline.plot(fig_dict, filename='random_walk.html')


if __name__ == '__main__':
    main()
