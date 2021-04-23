"""
Pierre-Charles Dussault
April 13, 2021

Building a world map for earthquakes with plotly
"""
import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


def main():

    # Explore the structure of the data.
    filename = 'data/eq_data_30_day_m1.json'
    with open(filename, 'r') as f_obj:
        all_eq_data = json.load(f_obj)

    chart_title = all_eq_data['metadata']['title']
    print(chart_title)

    # Where each item in the file inside 'features' is an earthquake...
    all_eq_dicts = all_eq_data['features']
    print('There were ' + str(len(all_eq_dicts)) + ' earthquakes.')

    magnitudes, longitudes, latitudes, hover_texts = [], [], [], []
    for each_feature in all_eq_dicts:
        magnitudes.append(each_feature['properties']['mag'])
        longitudes.append(each_feature['geometry']['coordinates'][0])
        latitudes.append(each_feature['geometry']['coordinates'][1])
        hover_texts.append(each_feature['properties']['title'])

    print(magnitudes[:10])
    print(longitudes[:5])
    print(latitudes[:5])

    # Map the earthquakes
    data = [{
        'type': 'scattergeo',
        'lon': longitudes,
        'lat': latitudes,
        'text':  hover_texts,
        'marker': {
            'size': [5*each_mag for each_mag in magnitudes],
            'color': magnitudes,
            'colorscale': 'Viridis',
            'reversescale': True,
            'colorbar': {'title': 'Magnitude'}
            }
        }]
    my_layout = Layout(title=chart_title)
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='global_earthquakes.html')


if __name__ == '__main__':
    main()
