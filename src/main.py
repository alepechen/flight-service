from fastapi import FastAPI, HTTPException
from services import flight_service
from utils import calculate_total_duration

app = FastAPI()

@app.get("/load-onward-flight/")
def load_flight_data():
    return flight_service.load_flight_data()

@app.get("/longest-flight")
def get_longest_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")

    longest = max(flights, key=calculate_total_duration)
    return longest

@app.get("/shortest-flight")
def get_shortest_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")

    shortest = min(flights, key=calculate_total_duration)
    return shortest