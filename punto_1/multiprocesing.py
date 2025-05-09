import time
import multiprocessing
from config import N, te, p



def tarea(i, te=te, p=p):
    t_paralelo = te * p
    t_secuencial = te * (1 - p)
    time.sleep(t_secuencial)
    time.sleep(t_paralelo)

def ejecutar_multiprocessing(n_workers):
    inicio = time.time()
    procesos = []

    for i in range(N):
        p = multiprocessing.Process(target=tarea, args=(i,))
        procesos.append(p)

    for i in range(0, N, n_workers):
        lote = procesos[i:i + n_workers]
        for p in lote:
            p.start()
        for p in lote:
            p.join()

    fin = time.time()
    return fin - inicio

