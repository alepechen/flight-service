from utils import parse_xml_files
from schemas import Flight, Itinerary, FlightResponse 

def load_flight_data(departure:str,destination:str):
    try:
        parsed = parse_xml_files("data")

        # Parse Onward Flights
        onward_flights_raw = parsed.get("Flights", {}) \
                                   .get("OnwardPricedItinerary", {}) \
                                   .get("Flights", {}) \
                                   .get("Flight", [])

        if isinstance(onward_flights_raw, dict):
            onward_flights_raw = [onward_flights_raw]

        onward_flights = [
            Flight(
                carrier=flight.get("Carrier", {}).get("#text", ""),
                carrier_id=flight.get("Carrier", {}).get("@id", ""),
                flight_number=flight.get("FlightNumber"),
                source=flight.get("Source"),
                destination=flight.get("Destination"),
                departure=flight.get("DepartureTimeStamp"),
                arrival=flight.get("ArrivalTimeStamp"),
                flight_class=flight.get("Class"),
                stops=int(flight.get("NumberOfStops", 0)),
                fare_basis=flight.get("FareBasis"),
                ticket_type=flight.get("TicketType"),
            )
            for flight in onward_flights_raw if flight.get("Source") == departure and flight.get("Destination") == destination
        ]
   
    except FileNotFoundError:
            print(f"File not found: {file_name}")  
    except Exception as e:
            print(f"Unexpected error with {file_name}: {e}")        

    return parsed
