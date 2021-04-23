"""
Pierre-Charles Dussault
March 24, 2021.

Exercise to explore and clean the data of a JSON file.
"""
import json


def main():

    # Explore the structure of the data.
    filename = 'data/eq_data_1_day_m1.json'
    with open(filename, 'r') as f_obj:
        all_eq_data = json.load(f_obj)

    # Where each item in the file inside 'features' is an earthquake...
    all_eq_dicts = all_eq_data['features']
    print('There were ' + str(len(all_eq_dicts)) + ' earthquakes.')

    magnitudes, longitudes, latitudes = [], [], []
    for each_feature in all_eq_dicts:
        tmp_mag = each_feature['properties']['mag']
        magnitudes.append(tmp_mag)
        tmp_lon = each_feature['geometry']['coordinates'][0]
        longitudes.append(tmp_lon)
        tmp_lat = each_feature['geometry']['coordinates'][1]
        latitudes.append(tmp_lat)

    print(magnitudes[:10])
    print(longitudes[:5])
    print(latitudes[:5])


if __name__ == '__main__':
    main()
