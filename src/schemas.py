from pydantic import BaseModel, Field
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

class ServiceCharge(BaseModel):
    type: str 
    charge_type: str
    amount: str
    
class Pricing(BaseModel):
    currency: str
    service_charges: List[ServiceCharge]

class Itinerary(BaseModel):
    flights: List[Flight] = Field(..., alias='Flights')
    pricing: Pricing = Field(..., alias='Pricing')
    class Config:
        populate_by_name = True

class FlightResponse(BaseModel):
    onward_itinerary: Optional[Itinerary]
    return_itinerary: Optional[Itinerary]