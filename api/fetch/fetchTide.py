#!/usr/bin/env python

# 10 requests per day
# Only need 1 per day as tide time don't change

from getData import fetchSimple
from loadConfig import loadConfig

keyEtc=loadConfig()

def tide(useenv):
    sgapikey={"prod": keyEtc["sgapikey3"], "DEBUG": keyEtc["sgapikey2"]}
    apikey=sgapikey[useenv]
    result=fetchSimple("https://api.stormglass.io/v2/tide/extremes/point",apikey,{
                            'lat': keyEtc["latitude"],
                            'lng': keyEtc["longitude"]
                            })
    return(result)

if __name__ == '__main__':
    print(tide())