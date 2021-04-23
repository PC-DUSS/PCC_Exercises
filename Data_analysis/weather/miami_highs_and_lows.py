"""
Pierre-Charles Dussault
March 23, 2021.

Compare Miami TMAX and TMIN from a weather file, using a class to extract the
data from the file, instead of doing it inside the main function.
"""
import matplotlib.pyplot as plt
from extracted_weather import ExtractedWeather


def main():
    """Main Program. This is a lot cleaner."""

    filename = 'data/miami_weather_2021_full.csv'
    # After the filename, accepts integer arguments representing, in that
    # order: (date_index, TMAX_index, TMIN_index) for the weather file.
    miami_extracted_weather = ExtractedWeather(filename)
    miami_dates = miami_extracted_weather.dates
    miami_highs = miami_extracted_weather.highs
    miami_lows = miami_extracted_weather.lows
    area_name = miami_extracted_weather.area_name

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(miami_dates, miami_highs, c='red', alpha=0.5)
    ax.plot(miami_dates, miami_lows, c='blue', alpha=0.5)
    
    plt.title('High and Low Daily Temperatures for ' + area_name +
              ' during 2021', fontsize=20)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Daily Temperature (F)', fontsize=16)
    ax.fill_between(miami_dates, miami_highs, miami_lows, alpha=0.15)

    plt.savefig('miami_highs_and_lows.png')
    plt.show()


if __name__ == '__main__':
    main()
