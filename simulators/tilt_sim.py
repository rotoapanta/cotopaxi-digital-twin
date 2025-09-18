# simulators/tilt_sim.py
import math, random
def gen_tilt(t):
    drift = 0.05 * math.sin(t/3600.0)  # deriva horaria
    tremor = random.gauss(0, 0.005)    # micro-ruido
    radial = 0.2 + drift + tremor      # grados
    tangential = 0.1 + 0.4*math.sin(t/1800.0) + random.gauss(0,0.005)
    return {"radial_deg": round(radial,4), "tangential_deg": round(tangential,4)}
