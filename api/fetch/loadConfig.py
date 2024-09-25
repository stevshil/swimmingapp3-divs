#!/usr/bin/env python

import os
from dotenv import load_dotenv

def loadConfig():
    fapi=open("keys/weatherapi.key","r")
    wapikey=fapi.readline().strip()
    fapi.close()
    # Stormglass
    fapi=open("keys/apikey.key","r")
    sgapikey=fapi.readline().strip()
    fapi.close()
    fapi=open("keys/apikey2.key","r")
    sgapikey2=fapi.readline().strip()
    fapi.close()
    flatlong=open("keys/latlong.data")
    latitude=flatlong.readline().strip()
    longitude=flatlong.readline().strip()
    location=flatlong.readline().strip()
    locationid=flatlong.readline().strip()
    areaid=locationid
    flatlong.close()
    gapi=open("keys/govapi.key","r")
    govapi=gapi.readline().strip()
    gapi.close()
    areas=open("keys/areaid","r")
    areaids=[]
    areaids=[x.strip() for x in areas.readlines()]
    areas.close()
    
    # System configuration
    load_dotenv()
    testState=os.getenv("MODE")
    configinfo={
        "HOURLY": os.getenv("HOURLY"),
        "DAILY": os.getenv("DAILY"),
        "TIDES": os.getenv("TIDES"),
        "SEWAGE": os.getenv("SEWAGE"),
        "WEATHER": os.getenv("WEATHER"),
        "SEATEMP": os.getenv("SEATEMP"),
        "DEBUG": os.getenv("DEBUG"),
        "SSL": os.getenv("SSL")
    }

    mainInfo={"sgapikey": sgapikey, "sgapikey2": sgapikey2, "latitude": latitude, "longitude": longitude, "location": location, "locationid": locationid, "gapi": gapi, "govapi": govapi, "areaid": areaid, "wapikey": wapikey, "testState": testState, "areaids": areaids, "configinfo": configinfo}

    return (mainInfo)

if __name__ == "__main__":
    print(loadConfig())