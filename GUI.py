# GUI.py
# Ventana del juego: dibujo de la matriz y herramientas de edición.
# NO conoce las reglas de la simulación: main.py le pasa la función 'paso'.

import tkinter as tk
from tkinter import filedialog, messagebox

import matriz as mz
import mapas
import Elementos_de_sonido as sonido

TAM_CANVAS = 600      # pixeles del área de dibujo
VELOCIDAD_MS = 50     # cada cuántos ms avanza la simulación


class Juego:
    def __init__(self, padre, matriz, paso, reiniciar, al_cerrar):
        """
        padre     -> ventana del menú (root)
        matriz    -> matriz con la que se empieza
        paso      -> función de main.py que avanza la simulación un tick
        reiniciar -> función de main.py que reinicia estados internos
        al_cerrar -> función de main.py que se llama al cerrar el juego
        """
        self.paso = paso
        self.reiniciar = reiniciar
        self.al_cerrar = al_cerrar

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Sandbox de Elementos")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.matriz = matriz
        self.n = len(matriz)
        self.elemento = mz.ARENA
        self.modo = "pincel"          # "pincel" o "rectangulo"
        self.inicio_rect = None
        self.pausado = False
        self.activo = True

        self.crear_interfaz()
        self.crear_celdas()
        self.ciclo()

    # ================= Interfaz =================
    def crear_interfaz(self):
        panel = tk.Frame(self.ventana, padx=8, pady=8)
        panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(panel, text="Elementos", font=("Arial", 11, "bold")).pack(anchor="w")
        for codigo in mz.SELECCIONABLES:
            tk.Button(panel, text=mz.NOMBRES[codigo], width=12, bg=mz.COLORES[codigo],
                      command=lambda c=codigo: self.elegir(c)).pack(pady=1)
        tk.Button(panel, text="Borrador", width=12,
                  command=lambda: self.elegir(mz.AIRE)).pack(pady=1)
        self.lbl_actual = tk.Label(panel, text="Actual: Arena")
        self.lbl_actual.pack(pady=4)

        tk.Label(panel, text="Pincel (celdas)").pack(anchor="w")
        self.pincel = tk.Scale(panel, from_=1, to=10, orient=tk.HORIZONTAL)
        self.pincel.set(2)
        self.pincel.pack(fill=tk.X)

        self.btn_modo = tk.Button(panel, text="Modo: Pincel", width=14, command=self.cambiar_modo)
        self.btn_modo.pack(pady=4)

        tk.Label(panel, text=f"N ({mz.N_MIN}-{mz.N_MAX})").pack(anchor="w")
        self.entrada_n = tk.Entry(panel, width=6)
        self.entrada_n.insert(0, str(self.n))
        self.entrada_n.pack(anchor="w")
        tk.Button(panel, text="Aplicar N", command=self.aplicar_n).pack(pady=2, anchor="w")

        tk.Button(panel, text="Guardar mapa", width=14, command=self.guardar).pack(pady=(10, 1))
        tk.Button(panel, text="Cargar mapa", width=14, command=self.cargar).pack(pady=1)
        tk.Button(panel, text="Limpiar mapa", width=14, command=self.limpiar).pack(pady=1)
        self.btn_pausa = tk.Button(panel, text="Pausar", width=14, command=self.pausar)
        self.btn_pausa.pack(pady=(10, 1))
        tk.Button(panel, text="Volver al menú", width=14, command=self.cerrar).pack(pady=(10, 1))

        self.canvas = tk.Canvas(self.ventana, width=TAM_CANVAS, height=TAM_CANVAS,
                                bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT)
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.bind("<B1-Motion>", self.arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)

    def crear_celdas(self):
        """Un rectángulo del canvas por cada casilla (se crean una sola vez)."""
        self.canvas.delete("all")
        self.tam_celda = TAM_CANVAS / self.n
        self.celdas = []
        for f in range(self.n):
            fila = []
            for c in range(self.n):
                x, y = c * self.tam_celda, f * self.tam_celda
                fila.append(self.canvas.create_rectangle(
                    x, y, x + self.tam_celda, y + self.tam_celda,
                    fill=mz.COLORES[mz.AIRE], outline=""))
            self.celdas.append(fila)
        self.dibujado = [[mz.AIRE] * self.n for _ in range(self.n)]
        self.dibujar()

    def dibujar(self):
        """Solo recolorea las casillas que cambiaron (mucho más rápido)."""
        for f in range(self.n):
            for c in range(self.n):
                codigo = self.matriz[f][c]
                if codigo != self.dibujado[f][c]:
                    self.canvas.itemconfig(self.celdas[f][c], fill=mz.COLORES[codigo])
                    self.dibujado[f][c] = codigo

    def poner_matriz(self, nueva):
        """Cambia la matriz completa (al cargar o cambiar N)."""
        self.matriz = nueva
        self.n = len(nueva)
        self.entrada_n.delete(0, tk.END)
        self.entrada_n.insert(0, str(self.n))
        self.reiniciar()
        self.crear_celdas()

    # ================= Mouse =================
    def pixel_a_celda(self, evento):
        return int(evento.y // self.tam_celda), int(evento.x // self.tam_celda)

    def clic(self, evento):
        fila, col = self.pixel_a_celda(evento)
        if self.modo == "pincel":
            mz.pintar_pincel(self.matriz, fila, col, self.elemento, self.pincel.get())
        else:
            self.inicio_rect = (fila, col)

    def arrastrar(self, evento):
        fila, col = self.pixel_a_celda(evento)
        if self.modo == "pincel":
            mz.pintar_pincel(self.matriz, fila, col, self.elemento, self.pincel.get())
        elif self.inicio_rect:
            self.canvas.delete("guia")
            f0, c0 = self.inicio_rect
            t = self.tam_celda
            self.canvas.create_rectangle(min(c0, col) * t, min(f0, fila) * t,
                                         (max(c0, col) + 1) * t, (max(f0, fila) + 1) * t,
                                         outline="yellow", tags="guia")

    def soltar(self, evento):
        if self.modo == "rectangulo" and self.inicio_rect:
            fila, col = self.pixel_a_celda(evento)
            f0, c0 = self.inicio_rect
            mz.pintar_rectangulo(self.matriz, f0, c0, fila, col, self.elemento)
            self.inicio_rect = None
            self.canvas.delete("guia")

    # ================= Botones =================
    def elegir(self, codigo):
        self.elemento = codigo
        sonido.reproducir("clic")
        nombre = "Borrador" if codigo == mz.AIRE else mz.NOMBRES[codigo]
        self.lbl_actual.config(text="Actual: " + nombre)

    def cambiar_modo(self):
        self.modo = "rectangulo" if self.modo == "pincel" else "pincel"
        self.btn_modo.config(text="Modo: Rectángulo" if self.modo == "rectangulo" else "Modo: Pincel")

    def aplicar_n(self):
        texto = self.entrada_n.get()
        if not texto.isdigit() or not mz.validar_n(int(texto)):
            messagebox.showerror("Error", f"N debe ser un entero entre {mz.N_MIN} y {mz.N_MAX}.",
                                 parent=self.ventana)
            return
        self.poner_matriz(mz.crear_matriz(int(texto)))

    def guardar(self):
        ruta = filedialog.asksaveasfilename(parent=self.ventana, defaultextension=".txt",
                                            filetypes=[("Mapa", "*.txt")])
        if ruta:
            mapas.guardar_mapa(self.matriz, ruta)

    def cargar(self):
        ruta = filedialog.askopenfilename(parent=self.ventana,
                                          filetypes=[("Mapa", "*.txt"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            nueva = mapas.cargar_mapa(ruta)
        except (ValueError, OSError) as error:
            messagebox.showerror("Archivo inválido", str(error), parent=self.ventana)
            return
        self.poner_matriz(nueva)

    def limpiar(self):
        mapas.limpiar_mapa(self.matriz)
        self.reiniciar()

    def pausar(self):
        self.pausado = not self.pausado
        self.btn_pausa.config(text="Reanudar" if self.pausado else "Pausar")

    def cerrar(self):
        self.activo = False               # detiene el ciclo
        self.ventana.destroy()
        self.al_cerrar(self.matriz)       # le devuelve el mundo a main.py

    # ================= Ciclo =================
    def ciclo(self):
        if not self.activo:
            return
        if not self.pausado:
            self.paso(self.matriz)
        self.dibujar()
        self.ventana.after(VELOCIDAD_MS, self.ciclo)
