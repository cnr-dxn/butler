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

from config import *

#-------------------------------------------------------------------------------------------------
# Microsoft Functions
def refreshAccessToken(refresh_token):
    token_response = app.acquire_token_by_refresh_token(refresh_token, scopes=scope)
    if "access_token" in token_response:
        return token_response["access_token"], token_response["refresh_token"]
    else:
        raise ValueError("Failed to refresh access token. Error: %s" % token_response.get("error"))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# ChatGPT Functions
def turnNewslettersToGPTResponse(raw_input):
    return raw_input

def createGreeting():
    return "Good morning. its whatever day it is"
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# MySQL Functions
def listOfIDS(connection = main_connection):
    query = """
        SELECT id FROM entries WHERE added_time >= NOW() - INTERVAL 5 DAY;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return [str(row[0]) for row in results]
    except Exception as e:
        print(f"get_recent_ids: unsuccessful due to {e}")
        return []
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# Email Functions
def extractTextFromHtml(html_content):
    return BeautifulSoup(html_content, 'html.parser').get_text(separator=' ', strip=True)

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