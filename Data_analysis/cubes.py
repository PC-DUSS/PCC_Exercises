'''
Pierre-Charles Dussault
March 11, 2021

Plot cubes for number from 1 to 5000.
Use a colormap
'''
import matplotlib.pyplot as plt


def main():
    x_values = range(1, 5001)
    y_values = [x**3 for x in x_values]

    fsize = 12
    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.viridis, s=10)

    ax.set_title("Scatter Plot of Cubic Numbers", fontsize=fsize*1.5)
    ax.set_xlabel("Base num", fontsize=fsize)
    ax.set_ylabel("Cube of Base num", fontsize=fsize)
    ax.tick_params(axis="both", which="major", labelsize=fsize)
    plt.show()


if __name__ == "__main__":
    main()
