"""
Pierre-Charles Dussault
March 22, 2021.

Plot the temperature highs and lows for Sitka, Alaska.
"""
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def main():
    """Main Program."""

    filename = 'data/sitka_weather_2018_simple.csv'
    with open(filename) as f_obj:
        reader = csv.reader(f_obj)
        header_row = next(reader)
        for index, each_header in enumerate(header_row):
            print(index, each_header)

        # Keep in mind the 'reader' will continue where it left off, so its
        # positionning according the previously written code is important to
        # the success of the following code.
        highs, lows, dates = [], [], []
        for each_row in reader:
            high = int(each_row[5])
            highs.append(high)
            date = datetime.strptime(each_row[2], '%Y-%m-%d')
            dates.append(date)
            low = int(each_row[6])
            lows.append(low)

        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(dates, highs, c='red', alpha=0.5)
        ax.plot(dates, lows, c='blue', alpha=0.5)
        plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

        fig.autofmt_xdate()
        plt.title('Daily high and low temperatures for 2018', fontsize=24)
        plt.xlabel('', fontsize=16)
        plt.ylabel('Temperature (F)', fontsize=16)
        plt.tick_params(labelsize=16)

        plt.show()


if __name__ == '__main__':
    main()
