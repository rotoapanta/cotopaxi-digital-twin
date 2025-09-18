# backend/app.py
from fastapi import FastAPI
from typing import List
from influx_client import query_range, last
app = FastAPI(title="Cotopaxi Digital Twin API")

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/last/{measurement}")
def last_point(measurement:str):
    return last(measurement)

@app.get("/range/{measurement}")
def range_points(measurement:str, start:str="-1h", station:str="COTO-N"):
    """
    start: ventana Influx (ej. -1h, -24h)
    """
    return query_range(measurement, start, station=station)

@app.get("/events")
def events(start:str="-24h"):
    return query_range("events", start, station="COTO-N")
