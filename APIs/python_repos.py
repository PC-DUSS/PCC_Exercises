"""
Pierre-Charles Dussault
April 19, 2021

Starting to learn how to work with APIs.
"""
import requests


def get_api_response(url, headers=None):
    return requests.get(url, headers=headers)


def get_dicts_of_repos(response_dict):
    return response_dict['items']


def display_repos_info(repo_dicts):
    print("\nSelected information about each repository.")
    for each_dict in repo_dicts:
        print(f"\nName: {each_dict['name']}")
        print(f"Owner: {each_dict['owner']['login']}")
        print(f"Stars: {each_dict['stargazers_count']}")
        print(f"Repository: {each_dict['html_url']}")
        print(f"Created: {each_dict['created_at']}")
        print(f"Updated: {each_dict['updated_at']}")
        print(f"Description: {each_dict['description']}")


def main():

    # Make an API call and store the response.
    url = 'https://api.github.com/search/repositories?q=language:python' \
          '&sort=stars'
    headers = {'Accept': 'application/vnd.github.com.v3+json'}
    my_request = get_api_response(url, headers)

    # Status code of 200 indicates success
    print(f"Status code: {my_request.status_code}")

    # Store API response in a variable.
    response_dict = my_request.json()
    print(f"response headers: {response_dict.keys()}")
    # Show total count of available python repositories.
    print(f"Total repositories: {response_dict['total_count']}")

    repo_dicts = get_dicts_of_repos(response_dict)
    # Show amount of repos returned.
    print(f"Repositories returned: {len(repo_dicts)}")

    display_repos_info(repo_dicts)


if __name__ == '__main__':
    main()
