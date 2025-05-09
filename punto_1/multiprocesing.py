import time
import multiprocessing

N = 25
te = 0.1
p = 1.0

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

if __name__ == "__main__":
    workers = 4
    tiempo = ejecutar_multiprocessing(workers)
    print(f"Tiempo con multiprocessing ({workers} workers): {tiempo:.4f} segundos")
