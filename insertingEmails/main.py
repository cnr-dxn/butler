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
    breakLine()

    main_connection.close()
    logEnd(service_name, start_time)