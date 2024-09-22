#!/usr/bin/env python

import sys
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
    except Exception:
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
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],1,"tides")
    try:
        data=loadFileData("TIDES")
        return data, 200
    except Exception:
        msg="Problem fetching TIDES data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404

@app.route("/tide/<tidedate>", methods=["GET"])
def tideHour(tidedate):
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["TIDES"],1,"tides")
    try:
        loadFileData("TIDES")
        data=present.getTideData(tidedate)
        return data, 200
    except Exception:
        msg="Problem fetching TIDES data - "+str(e)
        result={"ERROR": msg}
        return json.dumps(result), 404


@app.route("/sewage", methods=["GET"])
def sewage():
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage")
    print("DEBUG: "+result)
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
    runssl=False

    # Check if SSL directory exists
    try:
        if os.path('Certs/fullchain.pem'):
            runssl=True
            try:
                context = ('Certs/fullchain.pem', 'Certs/privkey.pem')
            except:
                context = None
        else:
            context = None
    except:
        context = None
    
    try:
        run_args=sys.argv
    except:
        run_args=[""]
        pass
    
    print("After SSL check: runssl: "+str(runssl))

    try:
        if sys.argv[1].upper() == "DEBUG":
            print("DEBUG")
            testState=keyEtc["testState"]
            print("Test State: "+testState)
            print("PORT: 5001")
            app.run(host='0.0.0.0',port=5001,debug=True)
        elif runssl == False:
            print("BASIC")
            print("PORT: 5001")
            serve(app, host='0.0.0.0', port=5001)
        else:
            print("SSL")
            print("PORT: 5001")
            serve(app, host='0.0.0.0', port=5001, url_scheme='https')
    except Exception as e:
        print(str(e))
        if runssl == False:
            print("BASIC")
            print("PORT: 5001")
            serve(app, host='0.0.0.0', port=5001)
        else:
            print("SSL")
            print("PORT: 5001")
            serve(app, host='0.0.0.0', port=5001, url_scheme='https')