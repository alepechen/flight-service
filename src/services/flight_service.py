from utils import parse_xml_files
from schemas import Flight, ServiceCharge, Pricing, Itinerary, FlightResponse 

def map_flight(raw: dict) -> Flight:
    return Flight(
        carrier=raw.get("Carrier", {}).get("#text"),
        carrier_id=raw.get("Carrier", {}).get("@id"),
        flight_number=raw.get("FlightNumber"),
        source=raw.get("Source"),
        destination=raw.get("Destination"),
        departure=raw.get("DepartureTimeStamp"),
        arrival=raw.get("ArrivalTimeStamp"),
        flight_class=raw.get("Class"),
        stops=int(raw.get("NumberOfStops", 0)),
        fare_basis=raw.get("FareBasis"),
        ticket_type=raw.get("TicketType")
    )

def load_flight_data()-> FlightResponse:

    try:
        parsed = parse_xml_files("data")

        data = parsed.get("PricedItineraries", {}) \
                                   .get("Flights", {})
        onward_flights = []
        
        for item in data:
            onward_priced_itinerary = item.get("OnwardPricedItinerary")
            pricing_data = item.get("Pricing")
            raw_flights = onward_priced_itinerary["Flights"]["Flight"]
            raw_flights = [f for f in raw_flights if isinstance(f, dict)]
            mapped_flights = [map_flight(f) for f in raw_flights]

            mapped_charges = [
                ServiceCharge(
                    type=ch["@type"],
                    charge_type=ch["@ChargeType"],
                    amount=ch["#text"]
                )
                for ch in pricing_data["ServiceCharges"]
            ] 
            pricing = Pricing(
                    currency=pricing_data["@currency"],
                    service_charges=mapped_charges
            )

            itinerary = Itinerary(
                    flights=mapped_flights,
                    pricing=pricing
            )
            onward_flights.append(itinerary)
   
    except Exception as e:
            print(f"Unexpected error: {e}")        
    return onward_flights

