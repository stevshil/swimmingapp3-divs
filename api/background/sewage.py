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

def getSewage(scheduler):
    thirty_minutes=60*30
    fifteen_minutes=60*15
    scheduler.enter(fifteen_minutes,1,getSewage, (scheduler,))
    result=fetch.performUpdate(keyEtc["testState"],keyEtc["configinfo"]["SEWAGE"],1,"sewage")
    print("DEBUG: "+result)
    print("Last run: "+datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M"))

print("Starting Sewage Data Gatherer at "+datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M"))
sewage_sched = sched.scheduler(time.time, time.sleep)
sewage_sched.enter(1,1,getSewage, (sewage_sched,))
sewage_sched.run()