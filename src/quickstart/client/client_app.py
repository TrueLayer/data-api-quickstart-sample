import json


class ClientCredentials:
    def __init__(self, filepath: str = "secrets.json") -> None:
        with open(filepath, "r") as f:
            secrets = json.load(f)
        self.client_id = secrets["client_id"]
        self.client_secret = secrets["client_secret"]
        self.redirect_uri = secrets["redirect_uri"]
