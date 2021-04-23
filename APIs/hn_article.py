"""
Pierre-Charles Dussault
April 20, 2021

Hacker News API exercise
"""
import requests
import json


def main():
    url = 'https://hacker-news.firebaseio.com/v0/item/19155826.json'
    r = requests.get(url)
    print(f"Status code: {r.status_code}")

    response_dict = r.json()
    readable_file = 'readable_hn_data.json'
    with open(readable_file, 'w') as f:
        json.dump(response_dict, f, indent=4)


if __name__ == '__main__':
    main()
