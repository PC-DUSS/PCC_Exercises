"""
Pierre-Charles Dussault
March 22, 2021.

Compare the daily temperature highs for Sitka, Alaska, and
Death Valley, California.
"""
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def pretty_print_header_row(station_name, header_row_name):
    """Pretty print the contents of a header row for a CSV reader"""
    print(station_name)
    for index, item in enumerate(header_row_name):
        print(index, item)


def main():
    """Main Program."""

    fname1 = 'data/sitka_weather_2018_full.csv'
    fname2 = 'data/death_valley_2018_full.csv'

    with open(fname1) as f_obj_sitka:
        with open(fname2) as f_obj_death_valley:
            # Create a file reader for each file.
            reader_sitka = csv.reader(f_obj_sitka)
            reader_death_valley = csv.reader(f_obj_death_valley)

            # Place each file reader on the first line of the files, and save
            # each of them as the file's header row.
            header_row_sitka = next(reader_sitka)
            header_row_death_valley = next(reader_death_valley)

            # Display each item and its index number in the header row list.
            pretty_print_header_row('Sitka, Alaska', header_row_sitka)
            pretty_print_header_row('Death Valley, California',
                                    header_row_death_valley)

            # Get information for the Sitka, Alaska weather station.
            sitka_dates, sitka_highs = [], []
            for each_row in reader_sitka:
                tmp_date = datetime.strptime(each_row[2], '%Y-%m-%d')
                if tmp_date < datetime.strptime('2019-01-01', '%Y-%m-%d'):
                    try:
                        tmp_temperature = int(each_row[8])
                    except ValueError:
                        pass
                    else:
                        sitka_dates.append(tmp_date)
                        sitka_highs.append(tmp_temperature)
                else:
                    break

            # Get information for the Death Valley, California weather station.
            death_valley_dates, death_valley_highs = [], []
            for each_row in reader_death_valley:
                tmp_date = datetime.strptime(each_row[2], '%Y-%m-%d')
                if tmp_date < datetime.strptime('2019-01-01', '%Y-%m-%d'):
                    try:
                        tmp_temperature = int(each_row[6])
                    except ValueError:
                        pass
                    else:
                        death_valley_dates.append(tmp_date)
                        death_valley_highs.append(tmp_temperature)
                else:
                    break

            # Create plots for both weather stations.
            plt.style.use('seaborn')
            fig, ax = plt.subplots(figsize=(16, 9))
            ax.plot(sitka_dates, sitka_highs, c='blue')
            ax.plot(death_valley_dates, death_valley_highs, c='red')

            # Format the plots' figure.
            plt.title('Comparison of daily temperature highs, between Sitka, '
                      'Alaska, and Death Valley, California.', fontsize=20)
            plt.xlabel('', fontsize=16)
            fig.autofmt_xdate()
            plt.ylabel('Daily Average Temperature', fontsize=16)
            ax.set_ylim(bottom=-10)

            # Show and save the figure
            plt.savefig('sitka_death_valley_compared.png')
            plt.show()


if __name__ == '__main__':
    main()
