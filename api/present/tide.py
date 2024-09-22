"""
Module to fetch tide temperature data based on hour provided
"""

from datetime import datetime
import sys
import json
sys.path.insert(0, '.')
from fetch import loadConfig

keyEtc=loadConfig()

def getTideData(curDate=datetime.strftime(datetime.now(),"%Y-%m-%d")):
    """
    Grab the data for the specified time.
    Uses server current hour if time not supplied.
    Client should provide hour to get the correct data for their timezone.
    """

    # curDate=datetime.strftime(datetime.now(),"%Y-%m-%d")

    print(keyEtc["configinfo"]["TIDES"])
    fh=open(keyEtc["configinfo"]["TIDES"],"r")
    data=json.load(fh)
    fh.close()

    result = [item for item in data["data"] if curDate in item["time"]]
    return json.dumps(result)

    # return(data["data"][hour])

if __name__ == "__main__":
    try:
        print(getTideData(sys.argv[1]))
    except:
        print(getTideData())