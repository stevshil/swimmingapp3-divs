#!/usr/bin/env python

# 1 million per month 
# 32 per day, only need hourly = 24

import sys
from getData import fetchSimple
from loadConfig import loadConfig

keyEtc=loadConfig()

def weather():
    result=fetchSimple("http://api.weatherapi.com/v1/forecast.json?q="+keyEtc["latitude"]+","+keyEtc["longitude"]+"&days=3&aqi=no&alerts=no,tides=no",keyEtc["wapikey"],None)
    return result

if __name__ == '__main__':
    print(weather())