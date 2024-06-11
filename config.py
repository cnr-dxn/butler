import msal # type: ignore 
import os
from typing import *
from twilio.rest import Client
from openai import OpenAI # type: ignore
import mysql.connector
import mysql.connector
import os

account_sid = os.environ['sid']
auth_token = os.environ['sec']
twilio_client = Client(account_sid, auth_token)

openai_client = OpenAI(api_key=os.environ['ope'])

client_id = os.environ['cli']
authority = "https://login.microsoftonline.com/common"  
scope = ["Mail.Read"]

app: msal.PublicClientApplication = msal.PublicClientApplication(client_id, authority=authority)

config = {
    "user": "cnrdxn",
    "password": os.environ["mys"],
    "host": "127.0.0.1",
    "database": "butler"
}

try:
    main_connection = mysql.connector.connect(**config)
    print("successfully connected to server")
except Exception as e:
    print(f"unsuccessful connection to the server: {e}")