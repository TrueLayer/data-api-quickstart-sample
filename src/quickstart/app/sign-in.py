import time
import urllib
from ..client.api import DataAPI
from ..client.account import Account
from ..client.credentials import UserCredentials
from ..client.client_app import ClientCredentials
from flask import Flask, redirect, request, url_for, render_template

# We need your client_id, client_secret and redirect_uri to interact with the Data API
# We read them from a configuration file, "secrets.json"
client_creds = ClientCredentials(filepath="secrets.json")
# Using ngrok the redirect uri would be something like
# 'https://5836b2bc.ngrok.io/signin_callback'
# It has to be authorized in TrueLayer's console!

app = Flask(__name__)
app.debug = True

# We will store data in a global variable - an in-memory database, if you like
# Do not do this is a real application!
# Data should be stored into a proper database.
CLIENT_DATA = {}

@app.route("/", methods=["GET"])
def sign_in():

    CLIENT_DATA = {}
    
    query = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": client_creds.client_id,
            # List of permissions https://docs.truelayer.com/#permissions
            "scope": "info cards accounts transactions balance offline_access direct_debits standing_orders products beneficiaries",
            "nonce": int(time.time()),
            "redirect_uri": client_creds.redirect_uri,
            "enable_mock": "true",
            "enable_open_banking_providers": "true",
            "enable_credentials_sharing_providers": "false",
        }
    )

    auth_uri = f"https://auth.truelayer.com/?{query}"
    return f'Connect you bank account <a href="{auth_uri}" target="_blank">here</a>'


# This is the endpoint that we told TrueLayer's AuthDialog to
# call once the authentication flow is complete.
# It will provide us with the `code` as a query parameter.
# We can then exchange this code to get an access token.
@app.route("/signin_callback", methods=["GET"])
def handle_signin():
    # Accessing query parameters in Flask
    authorization_code = request.args.get("code")

    user_creds = UserCredentials(client_credentials=client_creds)
    # We exchange the authorization code with a token
    user_creds.from_code(authorization_code)

    # We persist the user credentials in our in-memory database
    CLIENT_DATA["user_creds"] = user_creds

    return redirect(url_for("show_user_home"))


@app.route("/refresh_token")
def refresh_token():

    CLIENT_DATA["user_creds"].refresh_access_token()

    print("#### ", CLIENT_DATA["user_creds"].access_token)
    return redirect(url_for("show_user_home"))


# USER HOME PAGE
@app.route("/user_home")
def show_user_home():

    user_creds = CLIENT_DATA["user_creds"]

    api_client = DataAPI(credentials=user_creds)
    accounts = api_client.accounts()
    # We persist the user accounts in our in-memory database
    CLIENT_DATA["accounts"] = accounts

    # Get provider name from first account
    # first_account = list(accounts.values())[0]
    first_account = accounts[0]
    provider_id = first_account.provider.provider_id
    provider_name = first_account.provider.display_name

    # We persist the provider in our in-memory database
    CLIENT_DATA["provider_data"] = {
        "providername": provider_name,
        "providerid": provider_id,
    }

    # Render template
    return render_template(
        "user_home.html",
        client_data_provider=CLIENT_DATA["provider_data"],
        client_data_token=user_creds,
        accounts=accounts,
    )


# SHOW BALANCE
@app.route("/show_balance", methods=["GET"])
def show_balance():
    account_id = request.args.get("accountId")

    balance = Account.balance(CLIENT_DATA["user_creds"], account_id)
    account = [
        account
        for account in CLIENT_DATA["accounts"]
        if account.account_id == account_id
    ][0]
    # render accounts
    return render_template("accounts.html", account=account, balance=balance)


# SHOW TRANSACTIONS
@app.route("/show_transactions", methods=["GET"])
def show_transactions():
    account_id = request.args.get("accountId")

    transactions = Account.transactions(CLIENT_DATA["user_creds"], account_id)
    account = [
        account
        for account in CLIENT_DATA["accounts"]
        if account.account_id == account_id
    ][0]

    # render accounts
    return render_template(
        "transactions.html", account=account, transactions=transactions
    )
