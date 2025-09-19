from typing import Dict, List, Optional
from influxdb_client import InfluxDBClient
from settings import settings

# Preferir token si existe; si no, intentar basic auth con user/pass
if settings.influx_token:
    _client = InfluxDBClient(url=settings.influx_url,
                             token=settings.influx_token,
                             org=settings.influx_org)
else:
    _client = InfluxDBClient(url=settings.influx_url,
                             org=settings.influx_org,
                             username=settings.influx_user,
                             password=settings.influx_pass)

_query = _client.query_api()
_bucket = settings.influx_bucket

def last_point(measurement: str) -> Optional[Dict[str, float]]:
    q = f'''
    from(bucket:"{_bucket}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> last()
    '''
    tables = _query.query(q)
    values: Dict[str, float] = {}
    for t in tables:
        for r in t.records:
            fld = r.get_field()
            val = r.get_value()
            if isinstance(val, (int, float)):
                values[fld] = float(val)
    return values or None

def query_range_points(measurement: str, start: str, station: str) -> List[Dict]:
    q = f'''
    from(bucket:"{_bucket}")
      |> range(start: {start})
      |> filter(fn: (r) => r._measurement == "{measurement}")
      |> filter(fn: (r) => r.station == "{station}")
      |> keep(columns: ["_time","_field","_value"])
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> sort(columns: ["_time"])
    '''
    tables = _query.query(q)
    rows: List[Dict] = []
    for t in tables:
        for r in t.records:
            time_iso = r.get_time().isoformat()
            vals = {k: float(v) for k, v in r.values.items()
                    if (k not in ["result", "table", "_time"]
                        and isinstance(v, (int, float)))}
            rows.append({"time": time_iso, "values": vals})
    return rows
