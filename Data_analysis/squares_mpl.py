'''
Pierre-Charles Dussault
March 10, 2021

Example use of matplotlib.
'''
import matplotlib.pyplot as plt


def make_plot(value_list, title, xlabel, ylabel):
    '''
    Make and show a plot using a list of values.
    '''
    line_width = 3
    font_size = 14
    # Create appropriate list index numbering for the given value list,
    # starting with 1 instead of 0.
    index_of_values = []
    for i in range(1, len(value_list) + 1):
        index_of_values.append(i)
    # start creating the plot
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(index_of_values, value_list, linewidth=line_width)
    ax.set_title(title, fontsize=font_size*2)
    ax.set_xlabel(xlabel, fontsize=font_size)
    ax.set_ylabel(ylabel, fontsize=font_size)
    # set tickers
    ax.tick_params(axis="both", labelsize=font_size)
    # display the plot
    plt.show()


def main():
    squares = [1, 4, 9, 16, 25]
    make_plot(squares, "Square Numbers", "Base Value", "Square of Base Value")


if __name__ == "__main__":
    main()
