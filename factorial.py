"""
Pierre-Charles Dussault
April 26, 2021

Model the calculation of a factorial.
"""


def factorial(number):
    product = 1
    for i in range(number):
        product *= i + 1

    return product


def main():
    print(factorial(5))


if __name__ == "__main__":
    main()
