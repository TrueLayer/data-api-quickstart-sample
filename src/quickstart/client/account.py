import requests
from typing import NamedTuple, Optional, Dict, List
from undictify import type_checked_constructor
from .config import Config
from .credentials import UserCredentials
from .transaction import Transaction
from .provider import Provider
from .helpers import validate_dtformat


@type_checked_constructor()
class AccountNumber(NamedTuple):
    iban: Optional[str]
    number: str
    sort_code: str
    swift_bic: str


@type_checked_constructor()
class Account(NamedTuple):

    account_id: str
    account_type: str
    account_number: AccountNumber
    currency: str
    display_name: str
    provider: Provider
    update_timestamp: str

    @staticmethod
    def balance(creds: UserCredentials, account_id: str) -> Optional[Dict]:
        url = f"{Config.data_api_uri}/accounts/{account_id}/balance"
        headers = {"Authorization": f"Bearer {creds.access_token}"}
        r = requests.get(url, headers=headers)
        body = r.json()
        if body["status"] == "Succeeded":
            results = body["results"]
            assert len(results) == 1
            return results[0]

    @staticmethod
    def transactions(
        creds: UserCredentials,
        account_id: str,
        txn_from: str = None,
        txn_to: str = None,
    ) -> Optional[List[Transaction]]:
        """
        :param txn_from: YYYY-MM-DD
        :param txn_to: YYYY-MM-DD
        """
        if txn_from:
            validate_dtformat(txn_from)
        if txn_to:
            validate_dtformat(txn_to)
        url = f"{Config.data_api_uri}/accounts/{account_id}/transactions"
        payload = {"from": txn_from, "to": txn_to}
        headers = {"Authorization": f"Bearer {creds.access_token}"}
        r = requests.get(url, headers=headers, params=payload)
        body = r.json()
        if body["status"] == "Succeeded":
            results = body["results"]
            transactions = []
            for transaction in results:
                transactions.append(Transaction(**transaction))
            return transactions
