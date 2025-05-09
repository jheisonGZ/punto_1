import sys
import os
import tkinter as tk
from tkinter import messagebox
from seriall import ejecutar_serial
from multithreading import ejecutar_threading
from multiprocesing import ejecutar_multiprocessing
from Amdhl import amdahl_speedup
from config import N, te, p  # 'te' y 'p' solo se usan en la Ley de Amdahl

# Definir n_workers con un valor inicial
n_workers = 4  # Valor predeterminado, puedes cambiarlo según lo que necesites

# Función para cambiar parámetros
def cambiar_parametros():
    global N, te, p, n_workers
    try:
        # Crear una ventana para ingresar los nuevos parámetros
        def actualizar_parametros():
            global N, te, p, n_workers
            N = int(entry_N.get() or N)
            te = float(entry_te.get() or te)  # Solo afectará la Ley de Amdahl
            p = float(entry_p.get() or p)  # Solo afectará la Ley de Amdahl
            n_workers = int(entry_workers.get() or n_workers)
            
            # Actualiza también config.py
            with open("config.py", "w") as f:
                f.write(f"N = {N}\nte = {te}\np = {p}\n")

            messagebox.showinfo("Éxito", "Parámetros actualizados correctamente.")
            ventana_parametros.destroy()  # Cerrar la ventana

        ventana_parametros = tk.Toplevel()  # Crear una ventana emergente
        ventana_parametros.title("Cambiar Parámetros")
        ventana_parametros.configure(bg="#f0f8ff")

        tk.Label(ventana_parametros, text="Nuevo valor para N", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=0, pady=5, padx=10)
        tk.Label(ventana_parametros, text="Nuevo valor para te (solo para Amdahl)", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=0, pady=5, padx=10)
        tk.Label(ventana_parametros, text="Nuevo valor para p (solo para Amdahl)", bg="#f0f8ff", font=("Arial", 10)).grid(row=2, column=0, pady=5, padx=10)
        tk.Label(ventana_parametros, text="Nuevo número de workers", bg="#f0f8ff", font=("Arial", 10)).grid(row=3, column=0, pady=5, padx=10)

        entry_N = tk.Entry(ventana_parametros, font=("Arial", 10))
        entry_N.grid(row=0, column=1)
        entry_N.insert(0, str(N))  # Insertar el valor actual de N

        entry_te = tk.Entry(ventana_parametros, font=("Arial", 10))
        entry_te.grid(row=1, column=1)
        entry_te.insert(0, str(te))  # Insertar el valor actual de te (para Ley de Amdahl)

        entry_p = tk.Entry(ventana_parametros, font=("Arial", 10))
        entry_p.grid(row=2, column=1)
        entry_p.insert(0, str(p))  # Insertar el valor actual de p (para Ley de Amdahl)

        entry_workers = tk.Entry(ventana_parametros, font=("Arial", 10))
        entry_workers.grid(row=3, column=1)
        entry_workers.insert(0, str(n_workers))  # Insertar el valor actual de workers

        tk.Button(ventana_parametros, text="Actualizar", command=actualizar_parametros, bg="#4CAF50", fg="white", font=("Arial", 12), relief="solid").grid(row=4, column=1, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Entrada no válida. Intente de nuevo.")

# Función principal del menú con Tkinter
def main():
    def ejecutar_opcion(opcion):
        # Limpiar la pantalla de resultados
        result_label.config(text="")

        if opcion == '1':
            tiempo = ejecutar_serial()
            result_label.config(text=f"Tiempo en modo serial: {tiempo:.4f} segundos")

        elif opcion == '2':
            tiempo = ejecutar_threading(n_workers)
            result_label.config(text=f"Tiempo con threading ({n_workers} workers): {tiempo:.4f} segundos")

        elif opcion == '3':
            tiempo = ejecutar_multiprocessing(n_workers)
            result_label.config(text=f"Tiempo con multiprocessing ({n_workers} workers): {tiempo:.4f} segundos")

        elif opcion == '4':
            try:
                s = int(entry_s.get())  # Intentar obtener el número de procesadores
                resultado = amdahl_speedup(p, s)  # Solo en la Ley de Amdahl
                result_label.config(text=f"Speedup teórico con p={p} y s={s}: {resultado:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido de procesadores.")

        elif opcion == '5':
            cambiar_parametros()

        else:
            messagebox.showerror("Error", "Opción no válida. Intente de nuevo.")

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Ejecuciones")
    ventana.geometry("500x500")  # Ajusté el tamaño para que los botones se acomoden
    ventana.configure(bg="#f0f8ff")

    # Centrar la ventana en la pantalla
    window_width = 500
    window_height = 500
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Calcular la posición para centrar
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Establecer la geometría con la posición calculada
    ventana.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Título
    tk.Label(ventana, text="Sistema de Ejecuciones", font=("Arial", 16), bg="#f0f8ff", fg="#333").pack(pady=20)

    # Menú con botones coloridos
    tk.Button(ventana, text="Ejecutar en modo serial", command=lambda: ejecutar_opcion('1'), bg="#2196F3", fg="white", font=("Arial", 10), relief="solid", width=25).pack(pady=10)
    tk.Button(ventana, text="Ejecutar con threading", command=lambda: ejecutar_opcion('2'), bg="#FF9800", fg="white", font=("Arial", 10), relief="solid", width=25).pack(pady=10)
    tk.Button(ventana, text="Ejecutar con multiprocessing", command=lambda: ejecutar_opcion('3'), bg="#4CAF50", fg="white", font=("Arial", 10), relief="solid", width=25).pack(pady=10)
    tk.Button(ventana, text="Calcular speedup teórico (Ley de Amdahl)", command=lambda: ejecutar_opcion('4'), bg="#FF5722", fg="white", font=("Arial", 10), relief="solid", width=25).pack(pady=10)
    tk.Button(ventana, text="Cambiar parámetros", command=lambda: ejecutar_opcion('5'), bg="#9C27B0", fg="white", font=("Arial", 10), relief="solid", width=25).pack(pady=10)

    # Entrada para el número de procesadores en la opción 4
    tk.Label(ventana, text="Ingrese el número de procesadores (s):", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
    entry_s = tk.Entry(ventana, font=("Arial", 12))
    entry_s.pack(pady=5)

    # Etiqueta para mostrar los resultados
    result_label = tk.Label(ventana, text="", font=("Arial", 14), fg="blue", bg="#f0f8ff")
    result_label.pack(pady=20)

    # Iniciar la interfaz
    ventana.mainloop()

if __name__ == "__main__":
    main()
