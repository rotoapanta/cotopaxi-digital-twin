# backend/app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import os

import models
from influx_client import last_point, query_range_points

app = FastAPI(title="Cotopaxi Digital Twin API", version="0.1.0")

# CORS (necesario para que el frontend en :8080 consulte la API en :8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # en prod restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}

@app.get("/config/cesium-token")
def get_cesium_token():
    return {"token": os.getenv("CESIUM_ION_TOKEN", "")}

@app.get("/last/{measurement}", response_model=models.LastPoint)
def api_last_point(measurement: str):
    """
    Devuelve el último valor por field de un measurement (e.g. tilt, rain).
    Si no hay datos recientes, responde 404 con mensaje específico.
    """
    data = last_point(measurement)
    if not data:
        raise HTTPException(status_code=404, detail=f"No hay datos para {measurement}")
    return models.LastPoint(measurement=measurement, values=data)

@app.get("/range/{measurement}", response_model=List[models.SensorPoint])
def api_range_points(
    measurement: str,
    start: str = Query("-1h", description="Ventana Influx ej. -5m, -1h, -24h"),
    station: str = Query("COTO-N", description="Tag station"),
):
    rows = query_range_points(measurement=measurement, start=start, station=station)
    return [models.SensorPoint(time=r["time"], values=r["values"]) for r in rows]
