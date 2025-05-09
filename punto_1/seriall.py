import time

# Configuración
from config import N, te, p


def tarea(i, te=te, p=p):
    t_paralelo = te * p
    t_secuencial = te * (1 - p)
    time.sleep(t_secuencial)
    time.sleep(t_paralelo)

def ejecutar_serial():
    inicio = time.time()
    for i in range(N):
        tarea(i)
    fin = time.time()
    return fin - inicio


