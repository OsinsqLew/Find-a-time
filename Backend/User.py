import requests

class User:
    def __init__(self, username):
        self.username = username
        self.friendgroups = requests.get(f"http://localhost:8000/user_friendgroups/{username}").json().get("friend_groups", {})
        # self.availability = db.get_availability(self.username)