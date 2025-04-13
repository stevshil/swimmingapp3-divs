#!/bin/bash

# Script to ensure service is still running
# Uses .env file of the main python script

# Read .env file
. /$HOME/weather/.env

# Check URL connects
if ! curl -s --connect-timeout 10 $URL >/dev/null 2>&1
then
    echo "Weather service URL not responding" 1>&2
    cd $HOME/weather
    docker-compose restart
    curl -s -d "Weather service restarted $(date +'%H:%M %d/%m/%Y')" ntfy.sh/tpsweatherapp >/dev/null 2>&1
    exit 1
else
    echo "Weather service OK"
fi
