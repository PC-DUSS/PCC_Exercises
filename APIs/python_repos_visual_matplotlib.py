"""
Pierre-Charles Dussault
April 19, 2021

Starting to learn how to work with APIs.
"""
import requests

import matplotlib.pyplot as plt


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
    repo_names, stars = [], []
    for each_dict in repo_dicts:
        repo_names.append(each_dict['name'])
        stars.append(each_dict['stargazers_count'])

    # Make visualization.
    plt.barh(repo_names, stars, align='center', alpha=0.5)
    plt.yticks(repo_names, wrap=True)
    plt.xlabel('Stars')
    plt.title('Most-Starred Projects on Github')

    plt.show()


if __name__ == '__main__':
    main()
