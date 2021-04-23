"""
Pierre-Charles Dussault
March 11, 2021

Example scatter plot of a quadratic function.
"""

import matplotlib.pyplot as plt


def main():
    a = 3
    h = 7
    b = 1
    k = -11

    start_x = -100 + h
    end_x = 100 + h

    x_values = range(start_x, end_x)
    y_values = [a*(b*x-h)**2 + k for x in x_values]

    fsize = 10
    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, c='blue', s=10)

    ax.set_title("Fonction quadratique", fontsize=fsize*1.5)
    ax.set_xlabel("axe des abscisses", fontsize=fsize)
    ax.set_ylabel("axe des ordonnés", fontsize=fsize)
    ax.tick_params(axis="both", which="major", labelsize=fsize)
    plt.show()

if __name__ == "__main__":
    main()
