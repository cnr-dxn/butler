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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *

#-------------------------------------------------------------------------------------------------
# ChatGPT Functions
def turnToGPTResponse(raw_input: str) -> str:
    reversed = raw_input[::-1]
    return reversed[:500]

def createGreeting():
    return "Good morning. its whatever day it is"

def breakFunction():
    print("ill get to this later")
#-------------------------------------------------------------------------------------------------