#!/usr/bin/env python

from loadConfig import loadConfig
from getData import fetchSimple

# Run every 30 minutes

keyEtc=loadConfig()

def seaTemp(useenv):
    sgapikey={"prod": keyEtc["sgapikey"], "DEBUG": keyEtc["sgapikey2"]}
    apikey=sgapikey[useenv]
    passparams={'lat': keyEtc["latitude"], 'lng': keyEtc["longitude"], 'params': 'airTemperature,pressure,precipitation,waterTemperature,windDirection,windSpeed'}
    result=fetchSimple("https://api.stormglass.io/v2/weather/point",apikey,passparams)

    return result

if __name__ == "__main__":
    print(seaTemp("DEBUG"))