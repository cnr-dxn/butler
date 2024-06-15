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
def turnToGPTResponse(raw_input: str, real: bool) -> str:
    if ~real:
        print("freak out")
    else:
        print("we good")
    reversed = raw_input[::-1]
    return reversed[:500]

def createGreeting():
    return "Good morning. its whatever day it is"

def breakFunction():
    print("ill get to this later")
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