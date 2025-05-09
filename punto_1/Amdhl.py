import time
import multiprocessing
import statistics

# ------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------
N = 25         # Número total de tareas
te = 0.1       # Tiempo que duerme cada tarea (en segundos)
p = 0.7        # Fracción paralelizable (por defecto 70%)

# ------------------------------
# DEFINICIÓN DE LA TAREA
# ------------------------------
def tarea(i, te=te, p=p):
    # Simula una tarea con una parte secuencial y una parte paralela
    t_paralelo = te * p
    t_secuencial = te * (1 - p)
    time.sleep(t_secuencial)
    time.sleep(t_paralelo)

# ------------------------------
# IMPLEMENTACIÓN SERIAL
# ------------------------------
def ejecutar_serial():
    inicio = time.time()
    for i in range(N):
        tarea(i)
    fin = time.time()
    return fin - inicio

# ------------------------------
# FUNCION PARALELA CON MULTIPROCESSING
# ------------------------------
def ejecutar_paralelo(n_workers):
    inicio = time.time()
    procesos = []

    for i in range(N):
        p = multiprocessing.Process(target=tarea, args=(i,))
        procesos.append(p)

    for i in range(0, N, n_workers):
        lote = procesos[i:i+n_workers]
        for p in lote:
            p.start()
        for p in lote:
            p.join()

    fin = time.time()
    return fin - inicio

# ------------------------------
# MEDICIÓN DE TIEMPOS (4 ejecuciones, descarta el menor)
# ------------------------------
def medir_tiempos(ejecutar_funcion, n_workers):
    tiempos = [ejecutar_funcion(n_workers) for _ in range(4)]
    tiempos.sort()
    promedio = statistics.mean(tiempos[1:])  # descartar el menor
    return tiempos, promedio

# ------------------------------
# LEY DE AMDAHL (teórico)
# ------------------------------
def amdahl_speedup(p, s):
    return 1 / ((1 - p) + (p / s))

# ------------------------------
# EJECUCIÓN GENERAL
# ------------------------------
def main():
    T_serial = ejecutar_serial()
    print(f"Tiempo serial (1 worker): {T_serial:.4f} s")

    global p
    p = 0.7  # Fracción paralelizable

    print("\n--- Análisis con Amdahl (p=0.7) ---")
    for s in [2, 4, 8, 16]:
        tiempos, promedio = medir_tiempos(ejecutar_paralelo, s)
        emp_speedup = T_serial / promedio
        teo_speedup = amdahl_speedup(p, s)
        print(f"s={s}: Speedup empírico = {emp_speedup:.2f}, teórico (Amdahl) = {teo_speedup:.2f}")

if __name__ == "__main__":
    main()
