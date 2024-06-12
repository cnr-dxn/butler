import msal # type: ignore 
import requests # type: ignore
import pprint 
import json
import os
import sys
from typing import *
import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client
from openai import OpenAI # type: ignore
import mysql.connector
from mysql.connector.constants import ClientFlag

from LoggingFunctions import *
from config import *

#-------------------------------------------------------------------------------------------------

if "__main__":
    service_name = "Butler Service"
    start_time = logStart(service_name)

    new_access, new_refresh = refreshAccessToken(os.environ['ref'])

    runLoop(new_access)

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "commit":
            print("committing results!") 
            main_connection.commit()
        else:
            print("[INFO] argument is not 'commit'. not committing results")
    else:
        print("[INFO] no arguments passed. not committing results")

    main_connection.close()
    logEnd(service_name, start_time)

'''
PLAN:
    - get all emails for EITHER the last login date OR the past 4 days:
    - break down/filter it into sources (rn we got 2):
      - Radio Free Mobile
      - Compounded Daily
    - combine all threads of the same author (let's hardcode the author's in to a degree)

    - IF I ALWAYS STORE THE SCRIPTS, I CAN OVERWRITE THE MP3 WITH THE LATEST
    - will do this ^ with the recordings but nothing else (may not even store the recordings)

'''