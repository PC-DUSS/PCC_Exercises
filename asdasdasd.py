import matplotlib.pyplot as plt
import random

def main():
    """Main program"""
    # Fill a list with random integers between 1 and 100.
    this_list = [random.randint(1, 100) for i in range(100)]
    # Make a figure with a subplot.
    fig, ax = plt.subplots()
    # Plot all the points inside the list.
    ax.scatter(range(100), this_list, c='blue', s=10)
    # Display the plotted figure.
    plt.show()

if __name__ == '__main__':
    """Run only if executed as main program."""
    main()
