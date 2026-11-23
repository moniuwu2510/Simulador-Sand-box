"""
Proyecto II — Simulador Sandbox de Elementos
Tecnológico de Cartago - Escuela de Computadores
Grupo 2
Estudiantes: Mónica Blanco, Lucrecia Soto
"""

# main.py
# Menú principal e integración del sistema.
#   - Es el ÚNICO archivo que se ejecuta.
#   - Desde aquí se llama a todo: juego, cargar/guardar mapas, sonido e instrucciones.
#   - Controla las ventanas abiertas (no se abre la misma ventana dos veces).
#   - Junta los módulos de la simulación en una sola función: paso_simulacion().

import tkinter as tk
from tkinter import filedialog, messagebox

import matriz as mz
import mapas
import elementos
import interacciones
import plantas
import animales
import Elementos_de_sonido as sonido
from GUI import Juego


# ================= Integración de la simulación =================
def paso_simulacion(matriz):
    """Un tick del mundo. El orden importa: primero se mueven las cosas,
    después se aplican las transformaciones."""
    elementos.actualizar(matriz)
    interacciones.actualizar(matriz)
    plantas.actualizar(matriz)
    animales.actualizar(matriz)


def reiniciar_estados():
    """Se llama al limpiar o cargar un mapa: reinicia los estados internos."""
    elementos.reiniciar()
    interacciones.reiniciar()
    plantas.reiniciar()
    animales.reiniciar()


INSTRUCCIONES = """CÓMO JUGAR

• Elija un elemento en el panel izquierdo y dibuje con clic izquierdo.
  Mantenga presionado y arrastre para pintar varias celdas.
• Pincel: ajusta el tamaño del área cuadrada que se pinta.
• Modo Rectángulo: arrastre para llenar un área completa.
• Borrador: convierte las celdas en aire.
• N: tamaño del mundo (20 a 100).

ELEMENTOS
• Arena: cae y se desliza en diagonal.
• Agua: cae, fluye a los lados y se acumula.
• Piedra y Tierra: fijas; sirven para paredes y recipientes.
• Tierra + agua = pasto.
• Fuego: quema el pasto (lo vuelve tierra) y se apaga con agua.
• Semilla: cae y solo germina sobre pasto; la planta crece en 3 etapas.
• Animal: camina solo de izquierda a derecha, evita el agua y los obstáculos.

MAPAS
• Guardar / Cargar: archivos .txt con N y la matriz.
• Limpiar: deja todo en aire."""


# ================= Menú =================
class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sandbox de Elementos - Menú")
        self.root.resizable(False, False)

        self.matriz = mz.crear_matriz(mz.N_DEFECTO)   # el mundo actual
        self.ventanas = {}     # control de ventanas abiertas: nombre -> objeto
        self.juego = None

        self.crear_menu()

    def crear_menu(self):
        marco = tk.Frame(self.root, padx=40, pady=30)
        marco.pack()
        tk.Label(marco, text="SANDBOX DE ELEMENTOS", font=("Arial", 18, "bold")).pack(pady=(0, 20))

        botones = [
            ("Jugar", self.jugar),
            ("Cargar mapa", self.cargar),
            ("Guardar mapa", self.guardar),
            ("Sonido", self.abrir_sonido),
            ("Instrucciones", self.abrir_instrucciones),
            ("Salir", self.salir),
        ]
        for texto, funcion in botones:
            tk.Button(marco, text=texto, width=20, height=1, font=("Arial", 12),
                      command=funcion).pack(pady=4)

    # ---------- Control de ventanas ----------
    def ventana_abierta(self, nombre):
        """Si la ventana ya existe la trae al frente y devuelve True."""
        v = self.ventanas.get(nombre)
        if v is not None and v.winfo_exists():
            v.deiconify()
            v.lift()
            v.focus_force()
            return True
        return False

    # ---------- Juego ----------
    def jugar(self):
        sonido.reproducir("clic")
        if self.juego is not None:            # ya hay un juego abierto
            self.ventana_abierta("juego")
            return
        self.juego = Juego(self.root, self.matriz, paso_simulacion,
                           reiniciar_estados, self.al_cerrar_juego)
        self.ventanas["juego"] = self.juego.ventana
        self.root.withdraw()                   # esconde el menú mientras se juega

    def al_cerrar_juego(self, matriz):
        self.matriz = matriz                   # guarda el mundo como quedó
        self.juego = None
        self.root.deiconify()                  # vuelve a mostrar el menú

    # ---------- Mapas ----------
    def cargar(self):
        ruta = filedialog.askopenfilename(filetypes=[("Mapa", "*.txt"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            self.matriz = mapas.cargar_mapa(ruta)
        except (ValueError, OSError) as error:
            messagebox.showerror("Archivo inválido", str(error))   # no se cierra el programa
            return
        reiniciar_estados()
        messagebox.showinfo("Mapa cargado", f"Mapa de {len(self.matriz)}x{len(self.matriz)} cargado.")
        self.jugar()

    def guardar(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Mapa", "*.txt")])
        if ruta:
            mapas.guardar_mapa(self.matriz, ruta)
            messagebox.showinfo("Guardado", "Mapa guardado correctamente.")

    # ---------- Sonido ----------
    def abrir_sonido(self):
        if self.ventana_abierta("sonido"):
            return
        v = tk.Toplevel(self.root)
        v.title("Sonido")
        v.resizable(False, False)
        self.ventanas["sonido"] = v

        activo = tk.BooleanVar(value=sonido.activado)
        tk.Checkbutton(v, text="Sonido activado", variable=activo,
                       command=lambda: sonido.activar(activo.get())).pack(padx=20, pady=(15, 5))
        tk.Label(v, text="Volumen").pack()
        vol = tk.Scale(v, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                       command=sonido.cambiar_volumen)
        vol.set(sonido.volumen)
        vol.pack(padx=20)
        tk.Button(v, text="Cerrar", command=v.destroy).pack(pady=10)

    # ---------- Instrucciones ----------
    def abrir_instrucciones(self):
        if self.ventana_abierta("instrucciones"):
            return
        v = tk.Toplevel(self.root)
        v.title("Instrucciones")
        self.ventanas["instrucciones"] = v
        tk.Label(v, text=INSTRUCCIONES, justify="left", font=("Arial", 11),
                 padx=20, pady=15).pack()
        tk.Button(v, text="Cerrar", command=v.destroy).pack(pady=(0, 10))

    # ---------- Salir ----------
    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Menu(root)
    root.mainloop()
