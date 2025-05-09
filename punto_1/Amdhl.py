def amdahl_speedup(p, s):
    return 1 / ((1 - p) + (p / s))
