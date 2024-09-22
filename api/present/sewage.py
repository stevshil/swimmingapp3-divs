"""
Module to fetch sewage data based on hour provided
"""

from datetime import datetime
import sys
import json
sys.path.insert(0, '.')
from fetch import loadConfig

keyEtc=loadConfig()

def getSewageData():

    print(keyEtc["configinfo"]["SEWAGE"])
    fh=open(keyEtc["configinfo"]["SEWAGE"],"r")
    data=json.load(fh)
    fh.close()

    return json.dumps(data)

if __name__ == "__main__":
    print(getSewageData())