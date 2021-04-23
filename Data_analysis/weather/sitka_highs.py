"""
Pierre-Charles Dussault
March 22, 2021.

Plot the temperature highs from Sitka, Alaska.
"""
import csv
import matplotlib.pyplot as plt
from datetime import datetime


filename = 'data/sitka_weather_2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for index, each_header in enumerate(header_row):
        print(index, each_header)

    # Keep in mind the 'reader' will continue where it left off, so its
    # positionning according the previously written code is important to the
    # success of the following code.
    highs, dates = [], []
    for each_row in reader:
        high = int(each_row[5])
        highs.append(high)
        date = datetime.strptime(each_row[2], '%Y-%m-%d')
        dates.append(date)

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, highs, c='red')

    fig.autofmt_xdate()
    plt.title('Daily high temperatures for 2018', fontsize=24)
    plt.xlabel('', fontsize=16)
    plt.ylabel('Temperature (F)', fontsize=16)
    plt.tick_params(labelsize=16)

    plt.show()
