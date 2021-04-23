"""
Pierre-Charles Dussault
March 17, 2021.

Roll 2 D6 dice, calulating the sum of their values. Display the frequencies of
each resulting sum with matplotlib.
"""
import matplotlib.pyplot as plt
from die import Die


def main():

    die_1 = Die()
    die_2 = Die()
    num_of_rolls = 50000
    max_result = die_1.num_sides + die_2.num_sides
    results = [die_1.roll() + die_2.roll() for each_roll in
               range(num_of_rolls)]

    # For each possible result
    x = [i for i in range(2, max_result+1)]
    # Calculate its frequency
    frequencies = [results.count(value) for value in x]

    fig, ax = plt.subplots()
    ax.bar(x, frequencies)
    ax.set_title('Frequency of Sum Results when Throwing Two D6 Dice '
                 '50,000 Times')
    ax.set_xlabel('Result')
    ax.set_ylabel('Frequency')
    plt.savefig('d6_d6.png')
    plt.show()


if __name__ == '__main__':
    main()
