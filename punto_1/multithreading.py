import time
import threading
from config import N, te, p


def tarea(i, te=te, p=p):
    t_paralelo = te * p
    t_secuencial = te * (1 - p)
    time.sleep(t_secuencial)
    time.sleep(t_paralelo)

def ejecutar_threading(n_workers):
    inicio = time.time()
    threads = []

    for i in range(N):
        t = threading.Thread(target=tarea, args=(i,))
        threads.append(t)

    for i in range(0, N, n_workers):
        lote = threads[i:i + n_workers]
        for t in lote:
            t.start()
        for t in lote:
            t.join()

    fin = time.time()
    return fin - inicio

