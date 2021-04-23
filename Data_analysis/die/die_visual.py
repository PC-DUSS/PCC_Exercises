"""
Pierre-Charles Dussault
March 14, 2021

Visual testing for die module.

Roll multiple dice, multiple times, storing the result each time. Print the
results, then show an interactive histogram in a web browser.
"""
from plotly.graph_objs import Bar, Layout
from plotly import offline
from die import Die


def main():
    """Main program."""
    die1 = Die()
    die2 = Die(10)  # die2 will be 10-sided.

    results = []
    for roll_num in range(50000):
        result = die1.roll() + die2.roll()
        results.append(result)

    frequencies = []
    max_result = die1.num_sides + die2.num_sides
    for value in range(2, max_result+1):
        frequency = results.count(value)
        frequencies.append(frequency)

    # Visualize the results.
    x_values = list(range(2, max_result+1))
    data = [Bar(x=x_values, y=frequencies)]

    x_axis_config = {'title': 'Result of Roll', 'dtick': 1}
    y_axis_config = {'title': 'Frequency of Result'}
    my_layout = Layout(title='Results of rolling a D6 and D10 50000 times',
                       xaxis=x_axis_config, yaxis=y_axis_config)

    print(frequencies)
    offline.plot({'data': data, 'layout': my_layout}, filename='d6_d10.html')


if __name__ == "__main__":
    main()
