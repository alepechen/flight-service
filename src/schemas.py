from pydantic import BaseModel
from typing import Optional, List

class Flight(BaseModel):
    carrier: Optional[str]
    carrier_id: Optional[str]
    flight_number: Optional[str]
    source: Optional[str]
    destination: Optional[str] 
    departure: Optional[str]
    arrival: Optional[str]
    flight_class: Optional[str]
    stops: Optional[int] 
    fare_basis: Optional[str] 
    ticket_type: Optional[str]

class Itinerary(BaseModel):
    flights: List[Flight]


class FlightResponse(BaseModel):
    onward_itinerary: Optional[Itinerary]
    return_itinerary: Optional[Itinerary]