# simulators/infra_sim.py
import random
def gen_infrasound(t):
    base = abs(random.gauss(2, 1))
    burst = 0
    if random.random() < 0.02:  # 2% de prob de evento impulsivo
        burst = random.uniform(15, 60)
    return {"pa_rms": round(base,2), "pa_peak": round(base + burst, 2)}
