import requests
from typing import List, Optional
from .config import Config
from .credentials import UserCredentials
from .account import Account


class DataAPI:
    def __init__(self, credentials: UserCredentials) -> None:
        self.creds = credentials

    def identity(self):
        url = f"{Config.data_api_uri}/info"
        headers = {"Authorization": f"Bearer {self.creds.access_token}"}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        body = r.json()
        if body["status"] == "Succeeded":
            results = body["results"]
            return results
        else:
            return None

    def accounts(self) -> Optional[List[Account]]:
        url = f"{Config.data_api_uri}/accounts"
        headers = {"Authorization": f"Bearer {self.creds.access_token}"}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        body = r.json()
        if body["status"] == "Succeeded":
            results = body["results"]
            accounts = []
            for result in results:
                accounts.append(Account(**result))
            return accounts
        else:
            return None
