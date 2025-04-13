import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from datetime import timedelta

def get_tides(in_date=None):
    if in_date is None:
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

    return results  # Return the list of results for all days

if __name__ == "__main__":
    try:
        # Use todays date
        data = get_tides()
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(json.dumps(data, indent=4))  # Pretty-print the list as JSON
    except Exception as e:
        print(f"Error: {e}")