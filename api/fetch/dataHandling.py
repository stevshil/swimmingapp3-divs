"""
Module to retrieve the different API data.
API data will be stored in local JSON file.
"""

import os
from datetime import datetime
import shutil
from fetchSeaTeamp import seaTemp
from fetchSewage import getAllAlerts
from fetchTide import tide
from fetchWeather import weather
from loadConfig import loadConfig

keyEtc=loadConfig()

# Inputs api, file, frequency
def performUpdate(useenv,file_name,freq,api,*params):
    """
    Fetch data from APIs and store on server for cahced use
    """

    try:
        print("DEBUG ENV: "+usenv+" filename: "+file_name+" frequency: "+freq+" api: "+api+" params: "+params)
    except:
        pass

    # Check file state first
    if checkFileState(file_name,freq) == "OK" and api != "sewage":
        return "OK"

    # Determine which service to call
    if api == "seaTemp":
        result=seaTemp(useenv)
        if "error" in result:
            return "NOK: "+result
        else:
            return writeFileData(file_name,result)

    if api == "sewage":
        # result=govAlerts()
        # print("GovAlerts: "+str(result))
        result = getAllAlerts()
        return writeFileData(file_name,result)

    if api == "tides":
        # result=tide(useenv)
        result = tide(useenv)
        print("DEBUG TIDE: "+str(result))
        return writeFileData(file_name,result)

    if api == "weather":
        result=weather()
        return writeFileData(file_name,result)


def checkFileState(file_name,freq):
    """
    Check if the API data file needs to be updated
    """
    
    # Use of stat to check file modified time
    try:
        file_info = os.stat(file_name)
        mtime=file_info[8]
        diff_letter = ""
    except Exception:
        return "NEW"

    if freq == 1:
        diff_letter="%H"
    else:
        diff_letter="%d"

    # Check if it needs updating
    if datetime.now().strftime("%d") != datetime.fromtimestamp(mtime).strftime("%d"):
        return "UPDATE"
    
    if datetime.now().strftime(diff_letter) != datetime.fromtimestamp(mtime).strftime(diff_letter):
        return "UPDATE"
    else:
        return "OK"

def writeFileData(file_name,data):
    """
    Write the fetched data from the API service to the local disk for caching
    """
    
    nofile=0
    newfile=0

    try:
        shutil.copy(file_name,file_name+".old")
        newfile=1
    except Exception:
        # File does not exist
        nofile=1

    try:
        print("DEBUG FILENAME: "+str(file_name))
        fh=open(file_name,"w")
        fh.write(str(data))
        fh.close()
        if newfile == 1:
            os.remove(file_name+".old")
        fh.close()
        return "UPDATED"
    except Exception as e:
        try:
            fh.close()
        except:
            pass
        os.remove(file_name)
        if newfile == 1:
            os.remove(file_name+".old")
        if nofile == 1:
            shutil.copy(file_name+".old",file_name)
        return "NOK - "+str(e)

if __name__ == "__main__":
    import sys
    try:
        if sys.argv[1] == "sea":
            print(keyEtc["testState"],keyEtc["configinfo"]["SEATEMP"],1,"seaTemp")
            print(performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEATEMP"],1,"seaTemp"))
        if sys.argv[1] == "sewage":
            print(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage")
            print(performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage"))
        if sys.argv[1] == "tide":
            print(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],0,"tides")
            print(performUpdate(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],1,"tides"))
        if sys.argv[1] == "weather":
            print(keyEtc["testState"],keyEtc["configinfo"]["WEATHER"],1,"weather")
            print(performUpdate(keyEtc["testState"],keyEtc["configinfo"]["WEATHER"],1,"weather"))
    except Exception:
        print("No argument provided sea|sewage|tide|weather")