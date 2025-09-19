# simulators/generator.py
import time
from tilt_sim import gen_tilt
from gnss_sim import gen_gnss
from infra_sim import gen_infrasound
from rain_sim import gen_rain
from gas_sim import gen_gas
from utils import write_influx

STATIONS = ["COTO-N"]  # agrega COTO-S, COTO-E, COTO-W si quieres
PERIOD_S = 2

if __name__ == "__main__":
    while True:
        now = time.time()
        for st in STATIONS:
            tilt = gen_tilt(now)
            gnss = gen_gnss(now)
            infra = gen_infrasound(now)
            rain = gen_rain(now)
            gas = gen_gas(now)

            lahar_risk = (rain["rate_mm_h"] > 20.0)
            eruption_candidate = (gnss["uplift_mm"] > 5
                                  and gas["so2_ppm"] > 6
                                  and infra["pa_peak"] > 30)

            points = [
                ("tilt", {"station": st}, tilt),
                ("gnss", {"station": st}, gnss),
                ("infrasound", {"station": st}, infra),
                ("rain", {"station": st}, rain),
                ("gas", {"station": st}, gas),
            ]
            if lahar_risk:
                points.append(("events", {"source": "rule", "station": st},
                               {"score": 0.7, "type": "lahar_risk", "level": 1.0}))
            if eruption_candidate:
                points.append(("events", {"source": "rule", "station": st},
                               {"score": 0.9, "type": "eruption_candidate", "level": 2.0}))

            write_influx(points)
        time.sleep(PERIOD_S)
