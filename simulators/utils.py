import os, time
from influxdb_client import InfluxDBClient, Point, WriteOptions

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_USER = os.getenv("INFLUX_USER")
INFLUX_PASS = os.getenv("INFLUX_PASS")

if INFLUX_TOKEN:
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
else:
    client = InfluxDBClient(url=INFLUX_URL, org=INFLUX_ORG,
                            username=INFLUX_USER, password=INFLUX_PASS)

write_api = client.write_api(write_options=WriteOptions(batch_size=100, flush_interval=1000))

def write_influx(points):
    ts = int(time.time()*1e9)  # nanosegundos
    payload = []
    for measurement, tags, fields in points:
        p = Point(measurement)
        for k, v in tags.items(): p = p.tag(k, v)
        for k, v in fields.items():
            # Asegurar tipos numéricos
            if isinstance(v, (int, float)): p = p.field(k, v)
            else:
                try:
                    p = p.field(k, float(v))
                except Exception:
                    continue
        p = p.time(ts)
        payload.append(p)
    write_api.write(bucket=INFLUX_BUCKET, record=payload)
