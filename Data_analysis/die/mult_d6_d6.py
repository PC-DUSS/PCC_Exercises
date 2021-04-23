"""
Pierre-Charles Dussault
March 17 ,2021.

Roll two D6 dice 50,000 times. Multiply the value on each dice and store the
result. Visualize the frequency of results in an interactive web application.
"""
import plotly.graph_objs as go
from plotly import offline
import die


def main():

    d1 = die.Die()
    d2 = die.Die()
    max_result = d1.num_sides * d2.num_sides

    results = [d1.roll() * d2.roll() for i in range(50000)]

    frequencies = [results.count(value) for value in range(1, max_result+1)]

    x_values = list(range(1, max_result+1))
    data = go.Bar(x=x_values, y=frequencies)

    x_axis_config = {'title': 'Results', 'dtick': 1}
    y_axis_config = {'title': 'Frequency'}

    my_layout = go.Layout(title='Product of rolling two D6 '
                          'dice for 50,000 rolls.',
                          xaxis=x_axis_config,
                          yaxis=y_axis_config)
    offline.plot({'data': data, 'layout': my_layout},
                 filename='mult_d6_d6.html')


if __name__ == '__main__':
    main()
