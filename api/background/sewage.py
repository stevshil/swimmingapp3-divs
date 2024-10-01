#!/usr/bin/env python

# Script to run sewage from Beachbuoy every 30 minutes
# Beachbuoy API is massively slow, so trying to speed up this app

import sys, os
import json
from datetime import datetime
sys.path.insert(0, '.')
import fetch
import sched, time

keyEtc=fetch.loadConfig()

# open log file
# logfh = open("logs/sewage.log","w")

def getSewage(scheduler):
    sewint=int(keyEtc["configinfo"]["SEWAGEINT"])*60
    print("INTERVAL TIME: "+str(sewint))
    scheduler.enter(sewint,1,getSewage, (scheduler,))
    try:
        result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage")
        print("DEBUG: "+result, flush=True)
    except Exception as e:
        outerr="ERROR: "+str(e)
        # logfh.write(outerr)
        print(outerr, flush=True)
    output="Last run: "+datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    # logfh.write(output+"\n")
    print(output, flush=True)

output = "Starting Sewage Data Gatherer at "+datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
# logfh.write(output+"\n")
print(output, flush=True)
sewage_sched = sched.scheduler(time.time, time.sleep)
sewage_sched.enter(1,1,getSewage, (sewage_sched,))
sewage_sched.run()