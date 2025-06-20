#!/usr/bin/env python

import requests
import json
from datetime import datetime, timedelta
from loadConfig import loadConfig

# Run every 30 minutes

keyEtc=loadConfig()

def govAlerts():
    datenow=datetime.now()
    newdata=[]
    lastoutfall=""
    lastoutfalllocation=""
    for areaid in keyEtc['areaids']:
        response = requests.get('https://www.southernwater.co.uk/gateway/Beachbuoy/1.0/api/v1.0/Spills/GetHistoricSpills',
                            params={'areaid': areaid},
                            headers={'x-Gateway-APIKey': keyEtc["govapi"]})
        
        if response.status_code == 503:
            print("ERROR: API not responding "+str(response))
            return [{"bathingSite": "ERR", "eventStart": "ERR", "eventStop": "ERR", "activity": "API not responding", "duration-mins": 0, "impact": "NA", "outlet": "NA"}]

        if response.status_code == 200:
            json_data = response.json()
            data=json_data
            print("DEBUG: 200 OK")
            print("DEBUG: "+str(data))
            # print(datenow.strftime('%Y-%m-%d'))
            # Historical info
            for alert in data['items']:
                # print(alert)
                info={}
                impact="No"
                # Today
                try:
                    #print("IMPACT: "+str(alert["isImpacting"]))
                    info={'bathingSite': alert['bathingSite'], 'eventStart': alert['eventStart'], 'eventStop': alert['eventStop'], 'activity': alert['status'], 'duration-mins': alert['duration'], 'impact': impact, 'outlet': alert['outfallName']}
                    if alert['eventStop'] > lastoutfall:
                        lastoutfall=alert['eventStop']
                        lastoutfalllocation=alert['bathingSite']+" "+alert['outfallName']

                    if alert["isImpacting"] == False:
                        impact="No"
                    else:
                        impact="Yes"
                        
                    if datenow.strftime('%Y-%m-%d') in alert['eventStart']:
                        newdata.append(info)
                    elif datenow.strftime('%Y-%m-%d') in alert['eventStop']:
                        newdata.append(info)
                    # Yesterday
                    if (datenow+timedelta(days=-1)).strftime('%Y-%m-%d') in alert['eventStart']:
                        newdata.append(info)
                    elif (datenow+timedelta(days=-1)).strftime('%Y-%m-%d') in alert['eventStop']:
                        newdata.append(info)
                    if (datenow+timedelta(days=-2)).strftime('%Y-%m-%d') in alert['eventStart']:
                        newdata.append(info)
                    elif (datenow+timedelta(days=-2)).strftime('%Y-%m-%d') in alert['eventStop']:
                        newdata.append(info)
                except Exception as e:
                    print("EXCEPTION")
                    info={'bathingSite': alert['bathingSite'], 'eventStart': 'ERR', 'eventStop': 'ERR', 'activity': str(e), 'duration-mins': 0, 'impact': "NA", 'outlet': 'NA'}

        else:
            info={'bathingSite': alert['bathingSite'], 'eventStart': 'ERR', 'eventStop': 'ERR', 'activity': str(e), 'duration-mins': 0, 'impact': "NA", 'outlet': 'NA', 'lastoutfall': lastoutfall}
            newdata.append(info)
            print("ERROR: API not responding "+str(response))

    if len(newdata) == 0:
        newdata.append({'lastoutfall': lastoutfall, 'lastoutfalllocation': lastoutfalllocation})
        
    #print(newdata)
    return newdata

def govLive(areaid):
    # Live info
    newdata={}
    response = requests.get('https://www.southernwater.co.uk/gateway/Beachbuoy/1.0/api/v1.0/Spills',
                           headers={'x-Gateway-APIKey': keyEtc["govapi"]})

    # sitePeriods [] -> site {name: FOLKESTONE, id 12567, siteIcon, spillMessage}
    if response.status_code == 200:
        json_data = response.json()
        data=json_data
        for tmpdata in data['sitePeriods']:
            if tmpdata['site']['id'] == int(keyEtc["areaid"]):
                newdata['livespill'] = tmpdata['site']
    else:
        # newdata={"ERROR": "No data"}
        newdata={"livespill": {"id": 12567, "name": "FOLKESTONE", "bathingWaterId": 13, "latitude": 51.081959, "longitude": 1.1912825, "siteIcon": "0", "reviewStatus": "", "spillMessage":"ERROR FROM API DATA" }}
        

    return(newdata)

def getAllAlerts():
    alerts=govAlerts()
    lastoutfall=""

    # If no readings on last outfall do the following
    if 'lastoutfall' in alerts[0].keys():
        lastoutfall=alerts[0]
        alerts.pop(0)

    # live=govLive(keyEtc["locationid"])
    # return {"Alerts":alerts,"LiveAlert":live}
    # return json.dumps({"Alerts": alerts})
    return json.dumps({"Alerts": alerts, "updated": datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M"), "lastoutfall": lastoutfall})

if __name__ == '__main__':
    # print(govAlerts(keyEtc["locationid"]))
    # print(govLive(keyEtc["locationid"]))
    print(getAllAlerts())