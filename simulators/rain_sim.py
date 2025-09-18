# simulators/rain_sim.py
import random, math
def gen_rain(t):
    storm =  max(0, 30*math.sin(t/600.0)) if (int(t/600)%5==0) else 0
    rate = storm + random.random()*2
    mm = rate/60.0*2  # cada 2 s ~ aproximación
    return {"mm": round(mm,3), "rate_mm_h": round(rate,2)}
