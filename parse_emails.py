import msal # type: ignore 
import requests # type: ignore
import pprint 
import json
import os
from typing import *
import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client
from openai import OpenAI # type: ignore
import mysql.connector
from mysql.connector.constants import ClientFlag

#-------------------------------------------------------------------------------------------------

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
    print(f"nope: {e}")

#-------------------------------------------------------------------------------------------------

def refreshAccessToken(refresh_token):
    token_response = app.acquire_token_by_refresh_token(refresh_token, scopes=scope)
    if "access_token" in token_response:
        return token_response["access_token"], token_response["refresh_token"]
    else:
        raise ValueError("Failed to refresh access token. Error: %s" % token_response.get("error"))

def listOfIDS(connection = main_connection):
    currentCursor = connection.cursor()
    try: 
        currentCursor.execute(f"""
            SELECT id FROM entries WHERE added_time >= NOW() - INTERVAL 5 DAY;
        """)
        # print("returnDictGivenIndex: successful")
    except:
        print("listOfIDS: unsuccessful")
        print()
    new_urls = []
    urls = currentCursor.fetchall()
    for i in urls:
        new_urls.append(str(i[0]))
    return list(new_urls)
#-------------------------------------------------------------------------------------------------

def turnNewslettersToGPTResponse(raw_input):
    return raw_input

def createGreeting():
    return "Good morning. its whatever day it is"

def extractTextFromHtml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def extractAndPrepareEmails(emails, source = "Default"):
    master_script_input = []
    master_script_input_str = ""
    existing_emails = listOfIDS()

    for i in emails.get('value', []):
        email_body_raw = i.get('body', {}).get('content', '')
        email_sender = i.get("sender", "").get("emailAddress", "").get("address", "")
        email_subject = i.get("subject", "SUBJECT NOT FOUND")
        email_contents = extractTextFromHtml(email_body_raw)
        email_received_raw = i.get('receivedDateTime', "DATE NOT FOUND")
        email_received_date = email_received_raw.split('T')[0]
        email_received_time = email_received_raw.split('T')[1]
        email_id = i.get('id', "ID NOT FOUND")

        master_script_input.append(email_contents)

        print(f"Email {email_id}")
        print(f"- Source: {source}")
        print(f"- Subject: {email_subject}")
        print(f"- Sender: {email_sender}")
        print(f"- Received Date: {email_received_date}")
        print(f"- Received Time: {email_received_time}")
        print()
        # print(f"- Contents: {email_contents}")

        if email_id not in existing_emails:
            try:
                currentCursor = main_connection.cursor()
                currentCursor.execute("""
                    INSERT INTO entries (
                        id, 
                        source,
                        sender,
                        body, 
                        received_date, 
                        received_time 
                    ) VALUES (%s, %s, %s, %s, %s, %s)""", (
                        email_id,
                        source, 
                        email_sender, 
                        email_contents, 
                        email_received_date, 
                        email_received_time, 
                    )
                )
                print("successfully inserted:", email_id)
            except Exception as e:
                print("could not insert:", e)
        else:
            print(f"EMAIL ALREADY FOUND: {source}'s email '{email_subject}', sent on {email_received_date} at time {email_received_time}")
        main_connection.commit()
        break
    
    master_script_input_str = "\n".join(master_script_input)
    print(master_script_input_str)


# Use the access token to fetch emails
def fetchEmails(access_token):
    filters = [
        ("Myself", "from/emailAddress/address eq 'connorddixon@gmail.com'"),
        ("Radio Free Mobile", "from/emailAddress/address eq 'rhswindsor@gmail.com'"),
        ("How Money Works", "from/emailAddress/address eq 'news@compoundeddaily.com'")
    ]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    five_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=5)).isoformat() + 'Z'

    for i in filters:
        endpoint = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime ge {five_days_ago} and {i[1]}"
        response = requests.get(endpoint, headers=headers)
        emails_master = response.json()

        if response.status_code != 200:
            print(f"Error fetching emails: {emails_master}")
            # add text message once i get accepted
        else:
            extractAndPrepareEmails(emails_master, i[0])
        break

#-------------------------------------------------------------------------------------------------

if "__main__":
    # print("hello")
    # message = twilio_client.messages.create(body="does this work anymore", from_='+16203159839', to='+19702195822')
    new_access, new_refresh = refreshAccessToken(os.environ['ref'])
    # print("refrehsed")
    fetchEmails(new_access)
    main_connection.close()

'''
PLAN:
    - get all emails for EITHER the last login date OR the past 4 days:
    - break down/filter it into sources (rn we got 2):
      - Radio Free Mobile
      - Compounded Daily
    - combine all threads of the same author (let's hardcode the author's in to a degree)

'''