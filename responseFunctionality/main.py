import os
import sys
from typing import *
from twilio.rest import Client

from function import * # type: ignore
from MainFunctions import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *
from MainFunctions import *

#-------------------------------------------------------------------------------------------------

if "__main__":
    service_name = "Main Butler Service"
    start_time = logStart(service_name)

    mainLoop()

    commitOrNot(sys.argv)

    main_connection.close()
    logEnd(service_name, start_time)