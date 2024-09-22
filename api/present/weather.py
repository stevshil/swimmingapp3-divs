"""
Module to fetch weather data based on hour provided
"""

from datetime import datetime
import sys
import json
sys.path.insert(0, '.')
from fetch import loadConfig

keyEtc=loadConfig()

def getWeatherData(hour=datetime.now().hour):
    """
    Grab the data for the specified time.
    Uses server current hour if time not supplied.
    Client should provide hour to get the correct data for their timezone.
    """

    hour=int(hour)
    
    print(keyEtc["configinfo"]["WEATHER"])
    fh=open(keyEtc["configinfo"]["WEATHER"],"r")
    data=json.load(fh)
    fh.close()

    if hour < 0:
        hour = 0
    if hour > len(data["forecast"]["forecastday"][0]["hour"]):
        hour=len(data["forecast"]["forecastday"][0]["hour"])-1

    info = data["forecast"]["forecastday"][0]["hour"][hour]
    info2 = data["forecast"]["forecastday"][0]["day"]
    moon = data['forecast']['forecastday'][0]['astro']
    del info['time_epoch']
    result = {"weather": info, "overview": info2, "moon": moon}
    return json.dumps(result)

if __name__ == "__main__":
    print(getWeatherData(sys.argv[1]))