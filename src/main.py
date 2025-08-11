from fastapi import FastAPI, HTTPException
from services import flight_service

app = FastAPI()

@app.get("/load-onward-flight/{departure}/{destination}")
def load_flight_data(departure:str,destination:str):
    return flight_service.load_flight_data(departure, destination)