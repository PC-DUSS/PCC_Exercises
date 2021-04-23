"""
Pierre-Charles Dussault
April 15, 2021

Visualize 4.5M+ eartquakes around the world for the past 7 days.
"""
import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


def main():
    with open('data/4.5_week.geojson.json') as f:
        eq_data = json.load(f)

    chart_title = eq_data['metadata']['title']

    print(chart_title)
    print("There were " + str(len(eq_data['features'])) + " 4.5M+ earthquakes "
          "in the past 7 days.")

    magnitudes, longitudes, latitudes, hover_text = [], [], [], []
    for each_eq in eq_data['features']:
        magnitudes.append(each_eq['properties']['mag'])
        longitudes.append(each_eq['geometry']['coordinates'][0])
        latitudes.append(each_eq['geometry']['coordinates'][1])
        hover_text.append(each_eq['properties']['title'])

    print(magnitudes[:5])
    print(longitudes[:5])
    print(latitudes[:5])
    print(hover_text[:5])

    data = [{
        'type': 'scattergeo',
        'lon': longitudes,
        'lat': latitudes,
        'text': hover_text,
        'marker': {
            'size': [5*mag for mag in magnitudes],
            'color': magnitudes,
            'colorscale': 'viridis',
            'reversescale': True,
            'colorbar': {'title': 'Magnitude'}
            }
        }]
    my_layout = Layout(title=chart_title)
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='4.5M+_eqs_this_week.html')


if __name__ == '__main__':
    main()
