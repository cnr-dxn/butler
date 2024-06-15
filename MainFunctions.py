import os
from typing import *
import datetime

from config import *

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

def commitOrNot(sysargv):
    if len(sysargv) > 1:
        if sysargv[1].lower() == "commit":
            print("committing results!") 
            main_connection.commit()
        else:
            print("[INFO] argument is not 'commit'. not committing results")
    else:
        print("[INFO] no arguments passed. not committing results")
    breakLine()