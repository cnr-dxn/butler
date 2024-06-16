import requests # type: ignore
import os
import sys
from typing import *
import datetime
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *
from MainFunctions import *

#-------------------------------------------------------------------------------------------------
# ChatGPT Functions
def turnToGPTResponse(raw_input: str, real: bool = False) -> str:
    if ~real:
        print("not real")
    else:
        print("real")
    reversed = raw_input[::-1]
    return reversed[:500]

def createGreeting():
    return "Good morning. its whatever day it is"

def breakFunction():
    print("ill get to this later")
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# MySQL Functions
def selectMailBySender(sender: str, connection = main_connection):
    query = """
        SELECT sender, subject, received_date 
            FROM entries 
            WHERE sender = %s
            AND used = false;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sender, ))
            results = cursor.fetchall()
    except Exception as e:
        breakLine(False)
        print(f"[ERROR] get_recent_ids: unsuccessful due to {e}")
        breakLine()
        return []
    print(results)
#-------------------------------------------------------------------------------------------------

'''
Could not process parameters: str(news@compoundeddaily.com), it must be of type list, tuple or dict
'''