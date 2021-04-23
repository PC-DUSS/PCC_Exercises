"""
Pierre-Charles Dussault
April 19, 2021

Get most-starred projects on Github, but for Javascript.
"""
import requests

# Make an API call and store the response.
url = 'https://api.github.com/search/repositories?q=language:javascript' \
      '&sort=stars'
headers = {'Accept': 'application/vnd.github.com.v3+json'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")  # status code of 200 indicates success

# Store API response in a variable.
response_dict = r.json()
print(f"response headers: {response_dict.keys()}")

# Explore the information about the repositories.
print(f"Total repositories: {response_dict['total_count']}")
repo_dicts = response_dict['items']
print(f"Repositories returned: {len(repo_dicts)}")

print("\nSelected information about each repository.")
for each_dict in repo_dicts:
    print(f"\nName: {each_dict['name']}")
    print(f"Owner: {each_dict['owner']['login']}")
    print(f"Stars: {each_dict['stargazers_count']}")
    print(f"Repository: {each_dict['html_url']}")
    print(f"Created: {each_dict['created_at']}")
    print(f"Updated: {each_dict['updated_at']}")
    print(f"Description: {each_dict['description']}")
