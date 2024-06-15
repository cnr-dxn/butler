import os
import sys
from typing import *

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