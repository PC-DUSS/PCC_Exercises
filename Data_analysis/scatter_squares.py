'''
Pierre-Charles Dussault
March 11, 2021

Working with scatter plots.
'''
import matplotlib.pyplot as plt


x_values = range(1, 1001)  # list of numbers from 1 to 1000
y_values =[x**2 for x in x_values]  # list comprehensions are good, use them

plt.style.use("seaborn")
fig, ax = plt.subplots()

# You can use different color settings.
#
# c="a_color" --> change the entire plot with that color.
#
# c=(R,G,B) --> with RGB values between 0 and 1, 1 being light and 0 being dark.
#
# c=y_values, cmap=plt.cm.AColorMap --> gives a gradual color scheme to values,
#                                       can be used to emphasize higher or lower
#                                       values as desired.
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)

# set title, axis labels and parameters for the graduation ticks.
ax.set_title("Squares Scatter Plot", fontsize=24)
ax.set_xlabel("Base Value", fontsize=14)
ax.set_ylabel("Squared Value", fontsize=14)
ax.tick_params(axis="both", which="major", labelsize=14)

# set the range for each axis
ax.axis([0, 1000, 0, 1100000])

# plt.show()
# alternatively, you can save the figure instead of showing it
plt.savefig("scatter_squares.png", bbox_inches="tight")
