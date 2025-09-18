# simulators/gnss_sim.py
import random, math
COTO_LAT, COTO_LON, COTO_ALT = -0.680, -78.436, 5897  # aprox
def gen_gnss(t):
    uplift = 2.0 + 3.0*max(0, math.sin(t/7200.0)) + random.gauss(0,0.3)
    return {
        "lat": COTO_LAT + random.gauss(0, 1e-5),
        "lon": COTO_LON + random.gauss(0, 1e-5),
        "alt": COTO_ALT + random.gauss(0, 0.5),
        "uplift_mm": round(uplift, 2),
    }
