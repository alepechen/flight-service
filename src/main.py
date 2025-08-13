from fastapi import FastAPI, HTTPException
from services import flight_service
from utils import calculate_total_duration, calculate_price, calculate_optimal_score

app = FastAPI()

@app.get("/load-onward-flight/")
def load_flight_data():
    return flight_service.load_flight_data()

@app.get("/longest-flight")
def get_longest_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")
    valid_flights = [f for f in flights if calculate_total_duration(f) is not None]
    if not valid_flights:
        raise HTTPException(status_code=404, detail="No valid flights with duration")
    longest = max(valid_flights, key=calculate_total_duration)
    return longest

@app.get("/shortest-flight")
def get_shortest_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")
    valid_flights = [f for f in flights if calculate_total_duration(f) is not None]
    if not valid_flights:
        raise HTTPException(status_code=404, detail="No valid flights with duration")
    shortest = min(valid_flights, key=calculate_total_duration)
    return shortest

@app.get("/most-expensive")
def get_most_expensive_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")

    most_expensive = max(flights, key=calculate_price)
    return most_expensive

@app.get("/least-expensive")
def get_least_expensive_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")

    least_expensive = min(flights, key=calculate_price)
    return least_expensive

@app.get("/optimal-flight")
def get_optimal_flight():
    flights = flight_service.load_flight_data()
    if not flights:
        raise HTTPException(status_code=404, detail="No flights available")
    valid_flights = [f for f in flights if calculate_optimal_score(f) is not None]
    if not valid_flights:
        raise HTTPException(status_code=404, detail="No valid flights")
    optimal = min(valid_flights, key=calculate_optimal_score)
    return optimal
