# simulators/utils.py
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url=os.getenv("INFLUX_URL"),
                        token=os.getenv("INFLUX_TOKEN"),
                        org=os.getenv("INFLUX_ORG"))

write_api = client.write_api(write_options=SYNCHRONOUS)
bucket = os.getenv("INFLUX_BUCKET")

def write_influx(points):
    """Escribe una lista de puntos en InfluxDB"""
    pts = []
    for p in points:
        pts.append(Point(p[0]).tag(p[1].keys(), p[1].values()).field(p[2]))
    write_api.write(bucket=bucket, record=pts)
