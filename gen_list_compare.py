import sys


def main():
    nums_squared_list = [i ** 2 for i in range(10000)]
    nums_squared_gen = (i ** 2 for i in range(10000))
    print("Size of list" + "\n" + f"{sys.getsizeof(nums_squared_list)}")
    print("\nSize of generator" + "\n" + f"{sys.getsizeof(nums_squared_gen)}")


if __name__ == "__main__":
    main()
