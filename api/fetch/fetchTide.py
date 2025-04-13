#!/usr/bin/env python

# 10 requests per day
# Only need 1 per day as tide time don't change

from getData import fetchSimple
from loadConfig import loadConfig
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import requests
import json

keyEtc=loadConfig()

# def tide(useenv):
#     sgapikey={"prod": keyEtc["sgapikey3"], "DEBUG": keyEtc["sgapikey2"]}
#     apikey=sgapikey[useenv]
#     result=fetchSimple("https://api.stormglass.io/v2/tide/extremes/point",apikey,{
#                             'lat': keyEtc["latitude"],
#                             'lng': keyEtc["longitude"]
#                             })
#     return(result)

# def tidetimesorg(useenv):
def tide(useenv):
    in_date = datetime.now().strftime("%Y%m%d")  # Default to today's date in YYYYMMDD format
    results = []  # List to store tide data for each day
    for i in range(6):  # Loop from today to 5 days time (inclusive)
        current_date = (datetime.now() + timedelta(days=i)).strftime("%Y%m%d")
        url = "https://www.tidetimes.org.uk/folkestone-tide-times-" + current_date
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        tides_div = soup.find('div', id='tides')

        if not tides_div:
            results.append({"date": current_date, "error": "No div tides."})
            continue

        table = tides_div.find('table')
        if not table:
            results.append({"date": current_date, "error": "No table found."})
            continue

        rows_data = []  # List to store data for each row
        for tr in table.find_all('tr'):
            # Skip rows with class 'vis0'
            if 'vis0' in tr.get('class', []):
                continue
            if 'colhead' in tr.get('class', []):
                continue
            row_data = []
            for td in tr.find_all('td'):
                if 'NAVIGATION' in td.get_text(strip=True).upper():
                    continue
                text = td.get_text(strip=True)  # Get the text content of the <td>
                row_data.append(text)
            if row_data:  # Only add non-empty rows
                rows_data.append(row_data)
        if rows_data:
            results.append({"date": current_date, "data": rows_data})
        else:
            results.append({"date": current_date, "error": "No data found."})

    # results["updated"] = datetime.now().strftime('%Y-%m-%d')
    results = {"tide": results, "updated": datetime.now().strftime('%Y-%m-%d')}
    print(results)
    return json.dumps(results, indent=4)

if __name__ == '__main__':
    print(tide(keyEtc["testState"]))