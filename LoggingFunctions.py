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
# Member Functions
def breakLineSpecial(end: bool = True):
    print("=====================================================================================================")
    if end: print()

def breakLine(end: bool = True):
    print("*************************************************************************************")
    if end: print()

def logStart(script_name):
    breakLineSpecial(False)
    start_time = datetime.datetime.now()
    process_id = os.getpid()
    print(f"[INFO] {start_time.strftime('%Y-%m-%d %H:%M:%S')} - Script '{script_name}' started with PID {process_id}")
    breakLineSpecial()
    return start_time

def logEnd(script_name, start_time):
    breakLineSpecial(False)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = duration.microseconds // 1000
    
    print(f"[INFO] {end_time.strftime('%Y-%m-%d %H:%M:%S')} - Script '{script_name}' finished.")
    print(f"[INFO] Duration: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds, and {int(milliseconds)} milliseconds")
    breakLineSpecial()
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# Microsoft Functions
def refreshAccessToken(refresh_token):
    token_response = app.acquire_token_by_refresh_token(refresh_token, scopes=scope)
    if "access_token" in token_response:
        return token_response["access_token"], token_response["refresh_token"]
    else:
        raise ValueError("[FATAL] Failed to refresh access token. Error: %s" % token_response.get("error"))
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
        breakLine(False)
        print(f"[ERROR] get_recent_ids: unsuccessful due to {e}")
        breakLine()
        return []
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# Email Functions
def extractTextFromHtml(html_content):
    return BeautifulSoup(html_content, 'html.parser').get_text(separator=' ', strip=True)

def extractAndPrepareEmails(emails, source = "Default"):
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

        breakLine(False)
        print(f"[INFO] NEW EMAIL FOUND: {source}'s email with subject '{email_subject}', sent on {email_received_date} at time {email_received_time}")
        print(f"[INFO] - ID: {email_id}")
        print(f"[INFO] - Source: {source}")
        print(f"[INFO] - Subject: {email_subject}")
        print(f"[INFO] - Sender: {email_sender}")
        print(f"[INFO] - Received Date: {email_received_date}")
        print(f"[INFO] - Received Time: {email_received_time}")
        # print(f"[INFO] - Contents: {email_contents}")

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
                print(f"[INFO] SUCCESSFULLY INSERTED: {source}'s email '{email_subject}', sent on {email_received_date} at time {email_received_time}")
            except Exception as e:
                print(f"[ERROR] ERROR! COULD NOT INSERT: {source}'s email '{email_subject}', sent on {email_received_date} at time {email_received_time} due to: {e}")
        else:
            print(f"[INFO] EMAIL ALREADY FOUND: {source}'s email '{email_subject}', sent on {email_received_date} at time {email_received_time}")
        breakLine()
    
# Use the access token to fetch emails
def runLoop(access_token):
    filters = [
        ("Myself", "from/emailAddress/address eq 'connorddixon@gmail.com'"),
        ("Radio Free Mobile", "from/emailAddress/address eq 'rhswindsor@gmail.com'"),
        ("How Money Works", "from/emailAddress/address eq 'news@compoundeddaily.com'")
    ]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    five_days_ago = (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat() + 'Z'
    five_days_ago_readable = five_days_ago.split('T')[0] + " at " + (five_days_ago.split('T')[1]).split('.')[0] + " UTC"
    breakLine(False)
    print(f"[INFO] Fetching emails up until: {five_days_ago_readable}")
    breakLine()

    for i in filters:
        endpoint = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime ge {five_days_ago} and {i[1]}"
        response = requests.get(endpoint, headers=headers)
        emails_master = response.json()

        if response.status_code != 200:
            print(f"[ERROR] Error fetching emails: {emails_master}")
            # add text message once i get accepted
        else:
            extractAndPrepareEmails(emails_master, i[0])
        break

#-------------------------------------------------------------------------------------------------