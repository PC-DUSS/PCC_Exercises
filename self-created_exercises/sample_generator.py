"""
Pierre-Charles Dussault
May 3, 2021

Example of the use of Generators in Python
"""


def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


def is_num_palindrome(num):
    # Skip uni-digit numbers.
    if num // 10 == 0:
        return False

    tmp = num
    reversed_num = 0
    while tmp != 0:
        reversed_num = (reversed_num * 10) + (tmp % 10)
        tmp = tmp // 10

    if num == reversed_num:
        return num
    else:
        return False


def main():
    for i in infinite_sequence():
        pal = is_num_palindrome(i)
        if pal:
            print(pal)


if __name__ == "__main__":
    main()
