"""
Pierre-Charles Dussault
April 19, 2021

Starting to learn how to work with APIs.
"""
import requests

from plotly.graph_objs import Bar
from plotly import offline


def main():
    # Make an API call and store the response.
    url = 'https://api.github.com/search/repositories?q=language:python' \
        '&sort=stars'
    headers = {'Accept': 'application/vnd.github.com.v3+json'}
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}")  # status code of 200 means success

    # Process results.
    response_dict = r.json()
    repo_dicts = response_dict['items']

    repo_links, stars, labels = [], [], []
    for each_dict in repo_dicts:
        repo_name = each_dict['name']
        repo_url = each_dict['html_url']
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)

        stars.append(each_dict['stargazers_count'])

        owner = each_dict['owner']['login']
        description = each_dict['description']
        label = f"{owner}<br />{description}"
        labels.append(label)

    # Make visualization.
    data = [{
        'type': 'bar',
        'x': repo_links,
        'y': stars,
        'hovertext': labels,
        'marker': {
            'color': 'rgb(60, 100, 150)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
            },
        'opacity': 0.6,
        }]
    # notice we didn't import the Layout class, because we used a dictionary
    # approach to define our layout

    my_layout = {
            'title': 'Most-Starred Python Projects on Github',
            'titlefont': {'size': 28},
            'xaxis': {
                'title': 'Repository',
                'titlefont': {'size': 24},
                'tickfont': {'size': 14},
                },
            'yaxis': {
                'title': 'Stars',
                'titlefont': {'size': 24},
                'tickfont': {'size': 14},
                },
            }
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='python_repos_visualization.html')


if __name__ == '__main__':
    main()
