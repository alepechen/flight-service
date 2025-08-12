import os
import xmltodict
from datetime import datetime
from zoneinfo import ZoneInfo 

def parse_xml_files(folder: str = "data") -> dict:
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder '{folder}' not found.")

    parsed_data  = {}

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        # Only process XML files
        if os.path.isfile(file_path) and file_name.lower().endswith(".xml"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    xml_data = f.read()
                    parsed = xmltodict.parse(xml_data)
                    first_key = next(iter(parsed))
                    parsed_data= parsed[first_key]
                    # parsed_data = data.get("AirFareSearchResponse", {})
            except Exception as e:
                print(f"Failed to parse : {e}")

    return parsed_data 

airport_timezones = {
    "DEL": "Asia/Kolkata",
    "BOM": "Asia/Kolkata",
    "BLR": "Asia/Kolkata",
    "MAA": "Asia/Kolkata",
    "HYD": "Asia/Kolkata",
    "CCU": "Asia/Kolkata",
    "COK": "Asia/Kolkata",
    "CJB": "Asia/Kolkata",
    "DOH": "Asia/Qatar",
    "KUL": "Asia/Kuala_Lumpur",
    "DWC": "Asia/Dubai",
    "DXB": "Asia/Dubai",
    "BKK": "Asia/Bangkok",
    "XNB": "Asia/Dubai"
}

def parse_flight_time(time_str, airport_code):
    if not airport_timezones[airport_code]:
        print(f"No timezone for {airport_code}, defaulting to UTC.")
        tz = "UTC"
    else:
        tz = ZoneInfo(airport_timezones[airport_code])
    
    return datetime.strptime(time_str, "%Y-%m-%dT%H%M").replace(tzinfo=tz)

def calculate_total_duration(itinerary):
    first_flight = itinerary.flights[0]
    last_flight = itinerary.flights[-1]

    start = parse_flight_time(first_flight.departure, first_flight.source)
    end = parse_flight_time(last_flight.arrival, last_flight.destination)

    return int((end.astimezone(ZoneInfo("UTC")) - start.astimezone(ZoneInfo("UTC"))).total_seconds() / 60)

