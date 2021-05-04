"""
Pierre-Charles Dussault
April 20, 2021

Visualize the comment activity for the top articles at Hacker News.
"""
from operator import itemgetter
import requests

import numpy as np
import matplotlib.pyplot as plt


def get_sorted_articles():
    """
    Acquire a list of the top 30 articles at Hacker News, sorted by number of
    comments, in reverse order.
    """
    # Make an API request and store a list of all the received IDs for the
    # articles.
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    print(f"Status code: {r.status_code}")
    submission_ids = r.json()

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
        # Attempt to save the number of comments for each article.
        try:
            submission_dict['comments'] = response_dict['descendants']
        # Handle the case where there are no comments, by manually setting
        # the value to zero.
        except KeyError:
            submission_dict['comments'] = 0

        submission_dicts.append(submission_dict)

    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                              reverse=True)

    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion Link: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")

    return submission_dicts


def visualize_articles(article_dicts):
    """
    Make a bar-chart visualization of the top articles, from an article list,
    according to the number of comments each article has.
    """

    list_of_articles = []  # x
    list_of_comment_values = []  # y
    list_of_urls = []  # x-axis labels URLs (represents links to articles)
    for each_article in article_dicts:
        list_of_articles.append(each_article['title'])
        list_of_comment_values.append(each_article['comments'])
        list_of_urls.append(each_article['hn_link'])

    # Now create the bar chart
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.bar(list_of_articles, list_of_comment_values)  # (x, y)
    ax.set_title('Most popular articles on Hacker News, by number of comments')
    ax.set_ylabel('Comments')
    ax.set_xticks(np.arange(len(list_of_articles)))
    ax.set_xticklabels(list_of_articles, rotation=315, ha='left')

    # Set the URL for each label. The URL contains a link to the article.
    labels = ax.get_xticklabels()
    i = 0
    for each_label in labels:
        each_label.set_url(list_of_urls[i])
    # The link is not clickable on the graph created by Matplotlib. However, if
    # you save the plot to a file, it will be present in the file's metadata.

    plt.show()


def main():
    article_dicts = get_sorted_articles()
    visualize_articles(article_dicts)


if __name__ == '__main__':
    main()
