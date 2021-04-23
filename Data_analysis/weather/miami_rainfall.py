"""
Pierre-Charles Dussault
March 22, 2021.

Visualize rainfall in Miami, Florida, for the year 2021.
"""
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def main():
    """Main Program."""

    filename = 'data/miami_weather_2021_full.csv'
    with open(filename) as f_obj:
        reader = csv.reader(f_obj)
        header_row = next(reader)
        print(header_row)

        dates, precipitations = [], []
        for each_row in reader:
            today_date = datetime.strptime(each_row[2], '%Y-%m-%d')
            try:
                daily_prcp = each_row[3]
            except ValueError:
                print('There is no precipitation information for ' +
                      str(today_date))
            else:
                dates.append(today_date)
                precipitations.append(float(daily_prcp))

        fig, ax = plt.subplots()
        ax.plot(dates, precipitations, c='blue', alpha=0.5)
        plt.title('Miami, FL, 2021 Precipitations', fontsize=20)
        plt.xlabel('', fontsize=16)
        fig.autofmt_xdate()
        plt.ylabel('Precipitations', fontsize=16)
        plt.show()


if __name__ == '__main__':
    main()
