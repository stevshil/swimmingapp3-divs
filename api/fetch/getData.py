#!/usr/bin/env python

import requests
import json

# def fetchSimple(filename,url,apikey,inparams):
def fetchSimple(url,apikey,inparams):
    problem=""
    if inparams == None:
        try:
            response = requests.get(url,
                                headers={
                                'key': apikey
                                })
        except Exception as e:
            print("ERROR: "+str(e))
            problem=str(e)
    else:
        try:
            response=requests.get(url,
                            params=inparams,
                            headers={
                            'Authorization': apikey
                            })
        except Exception as e:
            print("ERROR: "+str(e))
            problem=str(e)
    
    if response.status_code == 200:
        json_data = json.dumps(response.json())
        data=json_data
        print(data)
    else:
        data="error"+" "+str(response.status_code)+" "+str(response.reason)+" "+problem
        print(data)
        
    if "error" not in data:
        # return False
        return data
    else:
        # if writeData(filename,data):
        #     return True
        # else:
        return data