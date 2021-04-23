"""
Pierre-Charles Dussault
March 22, 2021.

Plot high and low temperature values for Death Valley, California.
"""
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def main():
    """Main Program."""

    filename = 'data/death_valley_2018_simple.csv'
    with open(filename) as f_obj:
        reader = csv.reader(f_obj)
        header_row = next(reader)
        for index, each_header in enumerate(header_row):
            print(index, each_header)

        highs, lows, dates = [], [], []
        for each_row in reader:
            date = datetime.strptime(each_row[2], '%Y-%m-%d')
            try:
                high = int(each_row[4])
                low = int(each_row[5])
            except ValueError:
                print('Missing data for ' + str(date))
            else:
                highs.append(high)
                dates.append(date)
                lows.append(low)

        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(dates, highs, c='red', alpha=0.5)
        ax.plot(dates, lows, c='blue', alpha=0.5)
        plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

        fig.autofmt_xdate()
        plt.title('Daily high and low temperatures for 2018\nDeath Valley, CA',
                  fontsize=20)
        plt.xlabel('', fontsize=16)
        plt.ylabel('Temperature (F)', fontsize=16)
        plt.tick_params(labelsize=16)

        plt.show()


if __name__ == '__main__':
    main()
