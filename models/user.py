import datetime


class User:
    def __init__(self, username: str, password: str, token: str, token_activate_at: datetime.datetime):
        self.username = username
        self.password = password
        self.token = token
        self.token_activate_at = token_activate_at