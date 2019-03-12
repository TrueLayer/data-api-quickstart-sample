## TrueLayer Data API quickstart sample

### Overview
The following Python/Flask sample code shows a very basic integration against TrueLayer's Data API.
TrueLayer's Data API will be used to retrieve banking data for a single set of credentials: balance and transaction 
for each associated account or credit card. All endpoints require authorisation using an JWT access token.
To obtain an access token, an end-user has to give you consent to access their details for a given bank
using TrueLayer’s Auth Dialog, where they will be asked to enter their details.

This tutorial shows how to do this for a single set of credentials using a very rudimentary in-memory database (a Python
dictionary) to store user data.

### Registration and client credentials using TL's console
Go to <https://console.truelayer.com> and sign up: you need to get your `client_id` and `client_secret` - 
these are the keys that will be required to authenticate and interact with our API.

### Installation

#### Requirements
System requirements:
- python 3.7
- pip

#### Dev environment
Run the following command to reproduce the virtual environment required to run this example:
```bash
# We use pipenv to manage dependencies
pip install pipenv
# Recreate a virtual environment with the packages specified in Pipfile.lock
pipenv sync --dev
```

#### Launching the application

### Install ngrok
To get an access token, your end users will have to go through the Auth Dialog flow: this happens in a pop-up
using a Single Page Application hosted on TrueLayer's domain. Once the authentication flow has been successfully completed,
you will receive the access token at the callback endpoint you have specified when setting up your application (<https://console.truelayer.com/settings/application> > Redirect URIs).

For this process to work, your callback endpoint needs to be exposed on the public Internet because it needs to be reachable from our servers.

You can easily achieve this using ngrok, which will setup a local tunnel between your local development environment and
a temporary public URL.
Ngrok installation instruction can be found here <https://ngrok.com/download>. If you are running OSX, ngrok can just be installed using Homebrew: 
```bash
brew cask install ngrok
```
ngrok can then be run on a local port with: 
```bash
# 5000 is the local port we are using to run our Flask application
ngrok http 5000
```
In the output there will be a line with
```text
Forwarding                    https://<randomid>.ngrok.io -> localhost:5000
```
Copy the HTTPS URL, add `signin_callback` (e.g. `https://<randomid>.ngrok.io/signin_callback`) at the end and add it as redirect URI in 
<https://console.truelayer.com/settings/application> > Redirect URIs.

### Setting client keys
In the top folder of this project there is a file called `secrets.json`: you have to replace the provided
`client_id`, `client_secret` and `redirect_uri` with the secrets you got on TrueLayer's console as well as 
the URL provided by ngrok.
Once you have saved your changes, we can move forward

### Launching the application

You can now launch the application with a single command:
```bash
# FLASK_DEBUG=1 runs the application in the debug mode (more descriptive logs and error messages)
# You can use FLASK_DEBUG=0 to disable it
FLASK_DEBUG=1 FLASK_APP=src/quickstart/app/sign-in.py pipenv run flask run
```
The application will run on <http://localhost:5000>.
Visit <http://localhost:5000/signin> to try it out.


