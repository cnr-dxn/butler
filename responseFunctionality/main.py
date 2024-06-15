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

from function import * # type: ignore
from MainFunctions import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *
from MainFunctions import *

#-------------------------------------------------------------------------------------------------

if "__main__":
    service_name = "Butler Service"
    start_time = logStart(service_name)

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "commit":
            print("committing results!") 
            main_connection.commit()
        else:
            print("[INFO] argument is not 'commit'. not committing results")
    else:
        print("[INFO] no arguments passed. not committing results")
    breakLine()

    turnToGPTResponse("hello")

    main_connection.close()
    logEnd(service_name, start_time)