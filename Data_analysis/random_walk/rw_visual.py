"""
Pierre-Charles Dussault
March 11, 2021

Visual plotting of a random walk.
"""
import matplotlib.pyplot as plt

from random_walk import RandomWalk


def main():

    # While the program is active, keep making random walks.
    while True:
        # Make a random walk.
        rw = RandomWalk(5000)
        rw.fill_walk()

        # Create a subplot for the random walk.
        plt.style.use('classic')
        fig, ax = plt.subplots(figsize=(15, 9))

        # Plot the points visited during the walk.
        point_number = list(range(rw.num_points))
        ax.scatter(rw.x_values, rw.y_values, c=point_number,
                   cmap=plt.cm.Blues, edgecolors='none', s=10)

        # Plot the beginning and ending points with more contrast. Make sure to
        # plot these points at the end, just before calling plt.show(), to make
        # sure they appear on top of all the other points.
        ax.scatter(0, 0, c='white', s=100)
        ax.scatter(rw.x_values[-1], rw.y_values[-1], c='yellow', s=100)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.show()

        # Prompt user for another random walk.
        keep_running_program = input("Make another walk?: (y/n) >>")
        if keep_running_program == 'n':
            break


if __name__ == '__main__':
    main()
