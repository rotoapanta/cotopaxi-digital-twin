# simulators/generator.py
import time, random
from tilt_sim import gen_tilt
from gnss_sim import gen_gnss
from infra_sim import gen_infrasound
from rain_sim import gen_rain
from gas_sim import gen_gas
from utils import write_influx

STATION = "COTO-N"  # norte del cráter; añade más: COTO-S, COTO-W...
PERIOD_S = 2

if __name__ == "__main__":
    while True:
        t = time.time()
        tilt = gen_tilt(t)
        gnss = gen_gnss(t)
        infra = gen_infrasound(t)
        rain = gen_rain(t)
        gas = gen_gas(t)

        # Simple rule-based: lahar_risk si lluvia alta y tilt estable
        lahar_risk = (rain["rate_mm_h"] > 20.0)
        # eruption_candidate si uplift y SO2 suben y hay infrasonido impulsivo
        eruption_candidate = (gnss["uplift_mm"] > 5 and gas["so2_ppm"] > 6 and infra["pa_peak"] > 30)

        points = [
            ("tilt", {"station": STATION}, tilt),
            ("gnss", {"station": STATION}, gnss),
            ("infrasound", {"station": STATION}, infra),
            ("rain", {"station": STATION}, rain),
            ("gas", {"station": STATION}, gas),
        ]
        if lahar_risk:
            points.append(("events", {"source": "rule"}, {"type":"lahar_risk","level":"WARN","score":0.7}))
        if eruption_candidate:
            points.append(("events", {"source": "rule"}, {"type":"eruption_candidate","level":"ALERT","score":0.9}))

        write_influx(points)
        time.sleep(PERIOD_S)
