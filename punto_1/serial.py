import time

# Configuración
N = 25
te = 0.1
p = 1.0  # Fracción paralelizable

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

if __name__ == "__main__":
    tiempo = ejecutar_serial()
    print(f"Tiempo de ejecución serial: {tiempo:.4f} segundos")
