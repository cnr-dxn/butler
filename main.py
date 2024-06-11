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

from functions import *
from config import *

#-------------------------------------------------------------------------------------------------

if "__main__":
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