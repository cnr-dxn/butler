import os
import sys
from typing import *

from function import * # type: ignore
from MainFunctions import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *
from MainFunctions import *

#-------------------------------------------------------------------------------------------------

if "__main__":
    service_name = "Insert Email Service"
    start_time = logStart(service_name)

    new_access, new_refresh = refreshAccessToken(os.environ['ref'])

    runLoop(new_access)

    commitOrNot(sys.argv)

    main_connection.close()
    logEnd(service_name, start_time)