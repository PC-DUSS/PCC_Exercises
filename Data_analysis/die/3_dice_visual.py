"""
Pierre-Charles Dussault
March 17, 2021.

Roll 3 D6 dice 50,000 times and visualize the results using a histogram.
"""
from plotly.graph_objs import Bar, Layout
from plotly import offline
from die import Die


def main():
    d1 = Die()
    d2 = Die()
    d3 = Die()

    # Get all the results from the rolls.
    results = []
    for i in range(50000):
        result = d1.roll() + d2.roll() + d3.roll()
        results.append(result)

# Count the frequency of each obtained result.
    frequencies = []
    max_result = d1.num_sides + d2.num_sides + d3.num_sides
    for value in range(3, max_result+1):
        frequency = results.count(value)
        frequencies.append(frequency)

    x_values = list(range(3, max_result+1))
    data = [Bar(x=x_values, y=frequencies)]
    x_axis_config = {'title': 'Result of Roll', 'dtick': '1'}
    y_axis_config = {'title': 'Frequency'}
    my_layout = Layout(title='Results of rolling three D6\'s 50,000 times.',
                       xaxis=x_axis_config, yaxis=y_axis_config)
    offline.plot({'data': data, 'layout': my_layout},
                 filename='d6_d6_d6.html')


if __name__ == '__main__':
    main()
