import os
import xmltodict
from datetime import datetime
from zoneinfo import ZoneInfo 
from schemas import  Itinerary

def parse_xml_files(folder: str = "data") -> dict:
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder '{folder}' not found.")

    parsed_data  = {}

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(".xml"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    xml_data = f.read()
                    parsed = xmltodict.parse(xml_data)
                    first_key = next(iter(parsed))
                    parsed_data= parsed[first_key]

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

def parse_flight_time(time_str: str, airport_code: str) -> datetime:
    if not airport_timezones[airport_code]:
        print(f"No timezone for {airport_code}, defaulting to UTC.")
        tz = "UTC"
    else:
        tz = ZoneInfo(airport_timezones[airport_code])
    
    return datetime.strptime(time_str, "%Y-%m-%dT%H%M").replace(tzinfo=tz)

def calculate_total_duration(itinerary: Itinerary) -> int:
    if not itinerary.flights:
        return None
    first_flight = itinerary.flights[0]
    last_flight = itinerary.flights[-1]

    start = parse_flight_time(first_flight.departure, first_flight.source)
    end = parse_flight_time(last_flight.arrival, last_flight.destination)

    return int((end.astimezone(ZoneInfo("UTC")) - start.astimezone(ZoneInfo("UTC"))).total_seconds() / 60)

def calculate_price(itinerary: Itinerary) -> float:
    charges = itinerary.pricing.service_charges
    if not charges:
        return float('inf')
    total=charges[2].dict()['amount']
    return float(total)

MAX_DURATION = 48 * 60  # 48 hours in minutes
MAX_PRICE = 1000

def calculate_optimal_score(itinerary: Itinerary) -> float:
    if not itinerary.flights:
        return None
    duration = calculate_total_duration(itinerary)  
    price_ticket = calculate_price(itinerary)  
    price = float(price_ticket)           

    # Normalize
    norm_duration = min(duration / MAX_DURATION, 1.0)
    norm_price = min(price / MAX_PRICE, 1.0)

    # Combine both (equal weight)
    score = 0.5 * norm_duration + 0.5 * norm_price
    return score
