from datetime import datetime
import jwt
import requests
import humanize
from typing import Tuple
from .config import Config
from .client_app import ClientCredentials


class UserCredentials:
    def __init__(self, client_credentials: ClientCredentials) -> None:
        self.client_credentials = client_credentials
        self.access_token = None
        self.refresh_token = None
        self.credentials_id = None
        self.expiration_date = None

    def from_code(self, code: str) -> None:
        self.access_token, self.refresh_token = self._exchange_authorization_code(code)
        self._extract_info_from_token(access_token=self.access_token)

    def from_refresh_token(self, refresh_token: str) -> None:
        self.access_token, self.refresh_token = self._refresh_access_token(
            refresh_token
        )
        self._extract_info_from_token(access_token=self.access_token)

    def _extract_info_from_token(self, access_token: str) -> None:
        # The JWT is base64 encoded. We decode it and extract the infos inside it
        decoded = jwt.decode(access_token, verify=False)
        self.credentials_id = decoded["sub"]
        self.expiration_date = decoded["exp"]

    @property
    def lifetime(self) -> str:
        return humanize.naturaldelta(
            datetime.fromtimestamp(self.expiration_date) - datetime.now()
        )

    def refresh_access_token(self) -> None:
        if self.refresh_token is None:
            raise ValueError("We don't have a refresh token for this credentials!")
        self.access_token, self.refresh_token = self._refresh_access_token(
            self.refresh_token
        )

    def _exchange_authorization_code(self, code: str) -> Tuple[str, str]:
        params = {
            "grant_type": "authorization_code",
            "client_id": self.client_credentials.client_id,
            "client_secret": self.client_credentials.client_secret,
            "redirect_uri": self.client_credentials.redirect_uri,
            "code": code,
        }
        url = f"{Config.auth_server_uri}/connect/token"
        r = requests.post(url, data=params)
        r.raise_for_status()
        body = r.json()
        return body["access_token"], body["refresh_token"]

    def _refresh_access_token(self, refresh_token: str) -> Tuple[str, str]:
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_credentials.client_id,
            "client_secret": self.client_credentials.client_secret,
            "refresh_token": refresh_token,
        }
        url = f"{Config.auth_server_uri}/connect/token"
        r = requests.post(url, data=params)
        r.raise_for_status()
        body = r.json()
        return body["access_token"], body["refresh_token"]
