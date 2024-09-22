"""
Module to fetch sea temperature data based on hour provided
"""

from datetime import datetime
import sys
import json
sys.path.insert(0, '.')
from fetch import loadConfig

keyEtc=loadConfig()

def getSeaTempData(hour=datetime.now().hour):
    """
    Grab the data for the specified time.
    Uses server current hour if time not supplied.
    Client should provide hour to get the correct data for their timezone.
    """
    hour=int(hour)

    print(keyEtc["configinfo"]["SEATEMP"])
    fh=open(keyEtc["configinfo"]["SEATEMP"],"r")
    data=json.load(fh)
    fh.close()

    if hour < 0:
        hour = 0
    if hour > len(data["hours"]):
        hour=len(data["hours"])-1
    
    hour_data=data["hours"][hour]['waterTemperature']
    avg_temp=sum( list(hour_data.values()) ) / len(list(hour_data.values()))
    # print(hour_data)
    strTime=datetime.strptime(data["hours"][hour]["time"],"%Y-%m-%dT%H:%M:%S+00:00")
    result = {"seaTemp": round(avg_temp,2), "seaTime": datetime.strftime(strTime,"%d-%m-%Y %H:%M")}
    return json.dumps(result)

if __name__ == "__main__":
    print(getSeaTempData(sys.argv[1]))