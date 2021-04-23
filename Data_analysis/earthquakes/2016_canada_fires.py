"""
Pierre-Charles Dussault
April 15, 2021

Visualize fires in Canada for the year 2016.
"""
import csv
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


def main():

    with open('data/modis_2016_Canada.csv') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        brightnesses, longitudes, latitudes, hover_text = [], [], [], []
        for each_row in reader:
            brightnesses.append(float(each_row[2]))
            longitudes.append(float(each_row[1]))
            latitudes.append(float(each_row[0]))
            hover_text.append(str(each_row[5]) + ', ' + str(each_row[6]))

    data_dict = {
            'lon': longitudes,
            'lat': latitudes,
            'text': hover_text,
            'marker': {
                'size': [(each_bright/100)**2 for each_bright in brightnesses],
                'color': brightnesses,
                'colorscale': 'YlOrRd',
                'colorbar': {'title': 'Fire Brightness'}
                }
            }
    data = Scattergeo(data_dict)
    my_layout = Layout(title='Fires in Canada during 2016')
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='Canada_Fires_for_2016.html')


if __name__ == '__main__':
    main()
