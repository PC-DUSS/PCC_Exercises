"""
Pierre-Charles Dussault
April 20, 2021

Retrieve the top articles from Hacker News, and give a short summary for each
of them.
"""
from operator import itemgetter
import requests


def main():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    print(f"Status code: {r.status_code}")

    # In this case, the request returns only the IDs of the top stories,
    # not actually each individual story.
    submission_ids = r.json()
    print(submission_ids)  # as we can see with this

    submission_dicts = []
    for submission_id in submission_ids[:30]:
        # Now get each story with an individual API call.
        url = 'https://hacker-news.firebaseio.com/v0/item/' \
              f"{submission_id}.json"
        r = requests.get(url)
        print(f"ID: {submission_id}\tStatus: {r.status_code}")
        response_dict = r.json()

        # Build a dictionary for each response.
        submission_dict = {
                'title': response_dict['title'],
                'hn_link': 'http://news.ycombinator.com/'
                           f"item?id={submission_id}",
                }
        # Attempt to save the number of comments for each response.
        try:
            submission_dict['comments'] = response_dict['descendants']
        except KeyError:
            submission_dict['comments'] = 0
            pass

        submission_dicts.append(submission_dict)

    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), 
                              reverse=True)

    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion Link: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")


if __name__ == '__main__':
    main()
