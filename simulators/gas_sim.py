# simulators/gas_sim.py
import random, math
def gen_gas(t):
    so2 = 3 + 4*max(0, math.sin(t/5400.0)) + random.gauss(0,0.3)
    co2 = 420 + 10*math.sin(t/3600.0) + random.gauss(0,2)
    return {"so2_ppm": round(max(0,so2),2), "co2_ppm": round(co2,1)}
