"""
Pierre-Charles Dussault
April 15, 2021

Display available colorscales in plotly
"""
from plotly import colors


def main():
    """
    PLOTLY_SCALES is a dictionary containing all available colorscales.
    The 'keys()' method returns a list of only the keys from all the key-value
    pairs in the dictionary. The 'values()' method would return all the values
    from the key-value pairs, instead of the keys.
    """
    for key in colors.PLOTLY_SCALES.keys():
        print(key)

    for value in colors.PLOTLY_SCALES.values():
        print(value)


if __name__ == '__main__':
    main()
