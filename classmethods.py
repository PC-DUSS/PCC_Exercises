"""
Pierre-Charles Dussault
May 3, 2021

Exploring the classmethod decorator
"""


class Calculator():
    @classmethod
    def class_add(cls, a, b):
        return a + b

    @classmethod
    def class_subtract(cls, a, b):
        return a - b

    @classmethod
    def class_multiply(cls, a, b):
        return a * b

    @classmethod
    def class_divide(cls, a, b):
        return a / b

    def __init__(self):
        pass

    def instance_add(self, a, b):
        return a + b

    def instance_subtract(self, a, b):
        return a - b

    def instance_multiply(self, a, b):
        return a * b

    def instance_divide(self, a, b):
        return a / b


def main():
    print(Calculator.class_subtract(1, 5))
    print(Calculator().instance_subtract(1, 5))


if __name__ == "__main__":
    main()
