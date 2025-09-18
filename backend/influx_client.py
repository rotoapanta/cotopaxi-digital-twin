# backend/influx_client.py
import os
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url=os.getenv("INFLUX_URL"),
                        token=f"{os.getenv('INFLUX_USER')}:{os.getenv('INFLUX_PASS')}",
                        org=os.getenv("INFLUX_ORG"))
query_api = client.query_api()
bucket = os.getenv("INFLUX_BUCKET")

def last(measurement):
    q = f'''
    from(bucket:"{bucket}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> last()
    '''
    tables = query_api.query(q)
    out = {}
    for t in tables:
        for r in t.records:
            out.setdefault(r.get_field(), r.get_value())
    return out

def query_range(measurement, start, station):
    q = f'''
    from(bucket:"{bucket}")
      |> range(start: {start})
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> filter(fn: (r) => r.station == "{station}")
      |> keep(columns: ["_time","_field","_value"])
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    tables = query_api.query(q)
    res = []
    for t in tables:
        for r in t.records:
            res.append({"time":str(r["_time"]), **{k:r[k] for k in r.values.keys() if k not in ["_time"]}})
    return res
