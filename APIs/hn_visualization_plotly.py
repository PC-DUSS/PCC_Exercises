"""
Pierre-Charles Dussault
April 20, 2021

Visualize the most popular articles on Hacker News.
"""
import requests
from operator import itemgetter

from plotly.graph_objs import Bar
from plotly import offline


def get_sorted_articles():
    """
    Return a sorted list of article dictionaries.
    """
    # Make API call and store the received article IDs.
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)
    # Status code of 200 means success.
    print(f"Status code: {r.status_code}")
    response_ids = r.json()
    article_dicts = []

    for each_id in response_ids[:30]:
        # Now go through all IDs individually to get the article.
        url = f"https://hacker-news.firebaseio.com/v0/item/{each_id}.json"
        r = requests.get(url)
        # Display the status for each request.
        print(f"ID: {each_id}\tStatus: {r.status_code}")
        article_dict = r.json()

        # Build a formatted dictionary for each article.
        fmted_article_dict = {
            'title': article_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={each_id}",
            }
        try:
            fmted_article_dict['comments'] = article_dict['descendants']
        # If the article contains no comments, manually set its value to zero.
        except KeyError:
            fmted_article_dict['comments'] = 0

        article_dicts.append(fmted_article_dict)

    # Sort the article_dicts  by their number of comments, in decreasing order.
    article_dicts = sorted(article_dicts, key=itemgetter('comments'),
                           reverse=True)

    # Print a small summary of each article when all is finished.
    for each_article in article_dicts:
        print(f"\nTitle: {each_article['title']}")
        print(f"Discussion Link: {each_article['hn_link']}")
        print(f"Comments: {each_article['comments']}")

    return article_dicts


def visualize_articles(articles_list):
    """
    Throw plotly chart to visualize the given articles.
    """
    # Store the names of each article, and its respective number of comments,
    # each in a list.
    article_names, comment_nums, article_links, labels = [], [], [], []
    for each_article in articles_list:
        article_name = each_article['title']
        article_names.append(article_name)
        comment_num = each_article['comments']
        comment_nums.append(comment_num)
        # Create clickable links for each article.
        article_url = each_article['hn_link']
        article_link = f"<a href='{article_url}'>{article_name}</a>"
        article_links.append(article_link)

        # Create custom labels for each bar on the chart.
        label = f"{article_name}<br />comments: {comment_num}"
        labels.append(label)

    # Create the data set to visualize.
    data = [{
        'type': 'bar',
        'x': article_links,
        'y': comment_nums,
        'hovertext': labels,
        'marker': {
            'color': 'rgb(60, 100, 150)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
            },
        'opacity': 0.6,
        }]

    # Create the figure layout.
    my_layout = {
        'title': 'Top Articles on Hacker News, by Number of Comments',
        'titlefont': {'size': 28},
        'hoverlabel': {'bgcolor': 'rgb(25, 25, 25)'},
        'xaxis': {
            'title': 'Article',
            'titlefont': {'size': 20},
            'tickfont': {'size': 14},
            },
        'yaxis': {
            'title': 'Number of Comments',
            'titlefont': {'size': 20},
            'tickfont': {'size': 14},
            },
        }
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='hn_visual_plotly.html')


def main():
    sorted_articles = get_sorted_articles()
    visualize_articles(sorted_articles)


if __name__ == '__main__':
    main()
