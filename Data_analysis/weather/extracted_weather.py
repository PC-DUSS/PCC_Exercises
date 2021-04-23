"""
Pierre-Charles Dussault
March 23, 2021.

Module to handle data extraction from a weather CSv file.
"""
import csv
from datetime import datetime


class ExtractedWeather(object):
    
    def __init__(self, filename):
        self.filename = filename
        self.dates = []
        self.highs = []
        self.lows = []
        self._extract_weather_data()
    
    def _get_tag_indexes(self, reference_row):
        """Return the index numbers for 'name', 'date', 'TMAX' and 'TMIN' from
        a given reference row."""
        dict_of_indexes = {}
        for index, item in enumerate(reference_row):
            if item.lower() == 'name':
                dict_of_indexes['name_index'] = index
            elif item.lower() == 'date':
                dict_of_indexes['date_index'] = index
            elif item.upper() == 'TMAX':
                dict_of_indexes['TMAX_index'] = index
            elif item.upper() == 'TMIN':
                dict_of_indexes['TMIN_index'] = index

        return dict_of_indexes

    def _check_if_area_name_is_set(self, area_name, current_row,
                                   dict_of_indexes):
        """Check if the area_name list contains anything. If it is empty,
        save the weather station's name inside of it. Regardles of outcome,
        return the list."""
        name_index = dict_of_indexes['name_index']
        if not area_name:
            area_name.append(current_row[name_index])

        return area_name

    def _extract_weather_data(self):
        """Open file and extract the weather data."""
        with open(self.filename, 'r') as f_obj:
            reader = csv.reader(f_obj)
            # Display headers for the file.
            header_row = next(reader)
            print(header_row)
            
            # Get the proper index numbers for the relevant weather items.
            dict_of_indexes = self._get_tag_indexes(header_row)
            # Attribute the index numbers to more human-readable variables.
            self.name_index = dict_of_indexes['name_index']
            self.date_index = dict_of_indexes['date_index']
            self.TMAX_index = dict_of_indexes['TMAX_index']
            self.TMIN_index = dict_of_indexes['TMIN_index']

            # Now parse the file.
            area_name = []
            for each_row in reader:
                area_name = self._check_if_area_name_is_set(area_name,
                                                            each_row,
                                                            dict_of_indexes)
                tmp_date = datetime.strptime(each_row[self.date_index],
                                             '%Y-%m-%d')
                try:
                    tmp_high = float(each_row[self.TMAX_index])
                    tmp_low = float(each_row[self.TMIN_index])
                except ValueError:
                    print('No data for ' + each_row[self.date_index])
                else:
                    self.dates.append(tmp_date)
                    self.highs.append(tmp_high)
                    self.lows.append(tmp_low)

            self.area_name = area_name[0]
