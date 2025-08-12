from fastapi import FastAPI, HTTPException
from services import flight_service

app = FastAPI()

@app.get("/load-onward-flight/")
def load_flight_data():
    return flight_service.load_flight_data()