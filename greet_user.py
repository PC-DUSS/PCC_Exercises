

import json

filename = 'username.json'

try:
    with open(filename, 'r+') as f_obj:
        username = json.load(f_obj)
        print("Welcome back, " + username + "!")
except FileNotFoundError:
    with open(filename, 'w+') as f_obj:
        username = str(input("Please enter a username: "))
        print("Hello " + username)
        json.dump(username, f_obj)
