#!/usr/bin/env python

import sys, os
from flask import Flask
import json
from flask_cors import CORS
from waitress import serve
from datetime import datetime
sys.path.insert(0, '.')
import fetch
import present

keyEtc=fetch.loadConfig()

app = Flask(__name__)
CORS(app)

def loadFileData(apiFile):
    fh=open(keyEtc["configinfo"][apiFile],"r")
    data=json.load(fh)
    fh.close()
    return data

@app.route("/", methods=["GET"])
def index():
    testState=keyEtc["testState"]
    time_now = datetime.now()
    return_time = time_now.strftime("%Y-%m-%d %H:%M")
    return(json.dumps({"status": "OK", "time": return_time}))

@app.route("/weather", methods=["GET"])
def weather():
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["WEATHER"],1,"weather")
    try:
        data=loadFileData("WEATHER")
        return data, 200
    except Exception as e:
        msg="Problem fetching WEATHER data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404

@app.route("/weather/<hour>", methods=["GET"])
def weatherHour(hour):
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["WEATHER"],1,"weather")
    try:
        loadFileData("WEATHER")
        data=present.getWeatherData(hour)
        return data, 200
    except Exception:
        msg="Problem fetching WEATHER data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404

@app.route("/tide", methods=["GET"])
def tide():
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],0,"tides")
    try:
        data=loadFileData("TIDES")
        return data, 200
    except Exception as e:
        msg='[{"Error:", "Problem fetching TIDES data - '+str(e)+'"}]'
        result={"ERROR": msg}
        return json.dumps(result), 404

# @app.route("/tide/<tidedate>", methods=["GET"])
# def tideHour(tidedate):
#     result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],0,"tides")
#     try:
#         loadFileData("TIDES")
#         data=present.getTideData(tidedate)
#         return data, 200
#     except Exception:
#         msg="Problem fetching TIDES data - "+str(e)
#         result={"ERROR": msg}
#         return json.dumps(result), 404


@app.route("/sewage", methods=["GET"])
def sewage():
    # result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage")
    # print("DEBUG: "+result)
    # Background task now gets the data, see backgroun/sewage.py
    try:
        data=loadFileData("SEWAGE")
        return data, 200
    except Exception as e:
        msg="Problem fetching SEWAGE data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404
    
@app.route("/sea", methods=["GET"])
def sea():
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEATEMP"],1,"seaTemp")
    print("DEBUG: "+result)
    try:
        data=loadFileData("SEATEMP")
        return data, 200
    except Exception as e:
        msg="Problem fetching SEATEMP data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404

# Default route    
@app.route('/', defaults={'path': ''}, methods=["GET"])
@app.route('/<path:path>')
def catchall(path):
    testState=keyEtc["testState"]
    return(json.dumps({"status": "OK"}))


if __name__ == "__main__":
    #runssl=False
    runssl=keyEtc["configinfo"]["SSL"]
    testState=keyEtc["testState"]
    print("runssl: "+runssl)
    print("testState: "+testState)

    # Check if SSL directory exists
    try:
        print("Checking pems")
        if os.path.exists('Certs/fullchain.pem') and runssl == True:
            print("SSL is true")
            runssl=True
            try:
                context = ('Certs/fullchain.pem', 'Certs/privkey.pem')
            except Exception:
                context = None
        else:
            context = None
    except Exception:
        context = None
    
    try:
        run_args=sys.argv
    except Exception:
        run_args=[""]
        pass
    
    print("After SSL check: runssl: "+str(runssl))
    the_port = keyEtc["configinfo"]["PORT"]

    try:
        if testState.upper() == "DEBUG":
            print("Test State: "+testState)
            print(f"PORT: {the_port}")
            if runssl == True:
                print("WITH SSL")
                app.run(host='0.0.0.0',port=the_port,debug=True,ssl_context=context)
            else:
                app.run(host='0.0.0.0',port=the_port,debug=True)
        elif runssl == False:
            print("BASIC")
            print("PORT: {the_port}")
            serve(app, host='0.0.0.0', port=the_port)
        else:
            print("SSL")
            print(f"PORT: {the_port}")
            serve(app, host='0.0.0.0', port=the_port, url_scheme='https')
    except Exception as e:
        print(str(e))
        if runssl == False:
            print("BASIC")
            print(f"PORT: {the_port}")
            serve(app, host='0.0.0.0', port=the_port)
        else:
            print("SSL")
            print("PORT: ${the_port}")
            serve(app, host='0.0.0.0', port=the_port, url_scheme='https')