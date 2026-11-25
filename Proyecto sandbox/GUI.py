import tkinter as tk
from tkinter import filedialog, messagebox
import matriz as mz
import mapas
import Elementos_de_sonido as sonido
import animales
import plantas
import os
from PIL import Image, ImageTk
# variables globales de pixeles dibujados 
TAM_CANVAS = 600      # pixeles del área de dibujo
VELOCIDAD_MS = 50     # cada cuántos ms avanza la simulación
# clase juego con sus atributos y metodos
class Juego:
    def __init__(self, padre, matriz, paso, reiniciar, al_cerrar):
        self.paso = paso
        self.reiniciar = reiniciar
        self.al_cerrar = al_cerrar
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("MichiBox - Modo de juego")
        self.ventana.geometry("1100x800")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#29382B")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.matriz = matriz
        self.n = len(matriz)
        self.elemento = mz.ARENA
        self.modo = "pincel"          # "pincel" o "rectangulo"
        self.inicio_rect = None
        self.pausado = False
        self.activo = True

        self.sprites_originales = {}
        self.sprites = {}
        self.sprites_canvas = {}
        self.crear_interfaz()
        self.cargar_sprites()
        self.crear_celdas()
        self.ciclo()


    def crear_interfaz(self):
        imagen = Image.open("fondo_sandbox.png")
        imagen = imagen.resize((1100, 800))

        self.fondo = ImageTk.PhotoImage(
            imagen, master=self.ventana
        )

        self.canvas_fondo = tk.Canvas(
            self.ventana,
            width=1100,
            height=800,
            highlightthickness=0
        )

        self.canvas_fondo.place(x=0, y=0)

        self.canvas_fondo.create_image(
            0, 0,
            image=self.fondo,
            anchor="nw"
        )

        encabezado = tk.Frame(
            self.ventana,
            bg="#1C2920"
        )
        encabezado.place(
            x=0, y=0,
            width=1100, height=70
        )
        tk.Label(
            encabezado,
            text="MichiBox",
            font=("Impact", 32),
            bg="#1C2920",
            fg="#F3D391"
        ).place(x=25, y=5)
        tk.Label(
            encabezado,
            text="Crea tu propia aventura",
            font=("Segoe UI", 16, "bold"),
            bg="#1C2920",
            fg="white"
        ).place(x=780, y=20)

        panel = tk.Frame(
            self.ventana,
            bg="#3B4C35",
            bd=3,
            relief="ridge"
        )
        panel.place(
            x=20, y=90,
            width=370, height=620
        )
        tk.Label(
            panel,
            text="ELEMENTOS",
            font=("Impact", 22),
            bg="#3B4C35",
            fg="#F3D391"
        ).place(x=20, y=10)
         # Diccionarios de botones e imágenes
        self.botones_elementos = {}
        self.iconos_elementos = {}
        # Ruta de la carpeta de iconos
        carpeta_iconos = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "iconos"
        )
        # Generación de botones en dos columnas
        for i, codigo in enumerate(mz.SELECCIONABLES):
            fila = i // 2
            columna = i % 2
            # Obtener el nombre del elemento
            nombre = mz.NOMBRES[codigo]
            # Obtener la ruta de su imagen
            ruta = os.path.join(
                carpeta_iconos,
                nombre.lower() + ".png"
            )
            # Cargar y redimensionar el icono
            imagen = Image.open(ruta).convert("RGBA")
            imagen = imagen.resize(
                (32, 32),
                Image.Resampling.NEAREST
            )
            # Guardar la imagen para Tkinter
            self.iconos_elementos[codigo] = ImageTk.PhotoImage(
                imagen,
                master=self.ventana
            )
            # Crear el botón
            boton = tk.Button(
                panel,
                text=nombre,
                image=self.iconos_elementos[codigo],
                compound="left",
                font=("Impact", 14),
                bg="#263629",
                fg="white",
                activebackground="#789B58",
                activeforeground="white",
                relief="flat",
                bd=3,
                padx=8,
                cursor="hand2",
                command=lambda c=codigo: self.elegir(c)
            )

            boton.place(
                x=15 + columna * 170,
                y=60 + fila * 55,
                width=160,
                height=45
            )

            self.botones_elementos[codigo] = boton
        # Posición según la cantidad de elementos
        y_herramientas = 60 + (
            (len(mz.SELECCIONABLES) + 1) // 2
        ) * 55
        boton_borrador = tk.Button(
            panel,
            text="Borrador",
            command=lambda: self.elegir(mz.AIRE),
            font=("Impact", 15),
            bg="#DCC28A",
            fg="#29382B",
            relief="flat",
            cursor="hand2"
        )
        boton_borrador.place(
            x=15,
            y=y_herramientas,
            width=330,
            height=40
        )
        self.botones_elementos[mz.AIRE] = boton_borrador
        self.lbl_actual = tk.Label(
            panel,
            text="Actual: Arena",
            font=("Segoe UI", 13, "bold"),
            bg="#3B4C35",
            fg="#F3D391"
        )

        self.lbl_actual.place(
            x=15,
            y=y_herramientas + 45,
            width=330,
            height=30
        )
        # tamaño del pincel 
        tk.Label(
            panel,
            text="Tamaño del pincel",
            font=("Impact", 17),
            bg="#3B4C35",
            fg="white"
        ).place(
            x=15,
            y=y_herramientas + 80
        )
        self.pincel = tk.Scale(
            panel,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            bg="#3B4C35",
            fg="white",
            troughcolor="#1C2920",
            activebackground="#F3D391",
            highlightthickness=0,
            length=330,
            sliderrelief="flat"
        )
        self.pincel.set(2)
        self.pincel.place(
            x=15,
            y=y_herramientas + 110
        )
        # Modo de dibujo
        self.btn_modo = tk.Button(
            panel,
            text="Modo: Pincel",
            command=lambda: (
                sonido.reproducir("clic"),
                self.cambiar_modo()
            ),
            font=("Impact", 15),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            relief="flat",
            cursor="hand2"
        )
        self.btn_modo.place(
            x=15,
            y=y_herramientas + 170,
            width=330,
            height=40
        )
        tk.Label(
            panel,
            text=f"Tamaño N ({mz.N_MIN}-{mz.N_MAX})",
            font=("Segoe UI", 12, "bold"),
            bg="#3B4C35",
            fg="white"
        ).place(
            x=15,
            y=y_herramientas + 220
        )
        self.entrada_n = tk.Entry(
            panel,
            font=("Segoe UI", 14),
            justify="center",
            bg="#F0E9D6",
            fg="#29382B",
            relief="flat"
        )
        self.entrada_n.insert(0, str(self.n))
        self.entrada_n.place(
            x=15,
            y=y_herramientas + 250,
            width=100,
            height=40
        )
        tk.Button(
            panel,
            text="Aplicar N",
            command=lambda: (
                sonido.reproducir("clic"),
                self.aplicar_n()
            ),
            font=("Impact", 15),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            relief="flat",
            cursor="hand2"
        ).place(
            x=130,
            y=y_herramientas + 250,
            width=215,
            height=40
        )
# marco del juego 
        marco_simulacion = tk.Frame(
            self.ventana,
            bg="#1C2920",
            bd=4,
            relief="ridge"
        )

        marco_simulacion.place(
            x=430, y=90,
            width=620, height=620
        )

        # Canvas de la matriz
        self.canvas = tk.Canvas(
            marco_simulacion,
            width=TAM_CANVAS,
            height=TAM_CANVAS,
            bg="black",
            highlightthickness=0,
            cursor="crosshair"
        )

        self.canvas.place(x=6, y=6)

        # Eventos del ratón
        self.canvas.bind("<Button-1>", self.clic)
        self.canvas.bind("<B1-Motion>", self.arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)

# barra inferior de la ventana
        barra = tk.Frame(
            self.ventana,
            bg="#1C2920"
        )

        barra.place(
            x=0, y=730,
            width=1100, height=70
        )
        # Botón Pausar
        self.btn_pausa = tk.Button(
            barra,
            text="Pausar",
            command=lambda: (
                sonido.reproducir("clic"),
                self.pausar()
            ),
            font=("Impact", 15),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            relief="flat",
            cursor="hand2"
        )
        self.btn_pausa.place(
            x=15, y=12,
            width=200, height=45
        )
        # Botón Guardar
        tk.Button(
            barra,
            text="Guardar mapa",
            command=lambda: (
                sonido.reproducir("clic"),
                self.guardar()
            ),
            font=("Impact", 15),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            relief="flat",
            cursor="hand2"
        ).place(
            x=230, y=12,
            width=200, height=45
        )
        # Botón Cargar
        tk.Button(
            barra,
            text="Cargar mapa",
            command=lambda: (
                sonido.reproducir("clic"),
                self.cargar()
            ),
            font=("Impact", 15),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            relief="flat",
            cursor="hand2"
        ).place(
            x=445, y=12,
            width=200, height=45
        )
        # Botón Limpiar
        tk.Button(
            barra,
            text="Limpiar mapa",
            command=lambda: (
                sonido.reproducir("clic"),
                self.limpiar()
            ),
            font=("Impact", 15),
            bg="#A35C40",
            fg="white",
            activebackground="#C77D58",
            relief="flat",
            cursor="hand2"
        ).place(
            x=660, y=12,
            width=200, height=45
        )
        # Botón Volver al menú
        tk.Button(
            barra,
            text="Volver al menú",
            command=lambda: (
                sonido.reproducir("clic"),
                self.cerrar()
            ),
            font=("Impact", 15),
            bg="#79553D",
            fg="white",
            activebackground="#9A7454",
            relief="flat",
            cursor="hand2"
        ).place(
            x=875, y=12,
            width=210, height=45
        )
        # Destacar el elemento inicial
        self.botones_elementos[self.elemento].config(
            bg="#F3D391",
            fg="#29382B",
            relief="sunken"
        )

    def cargar_sprites(self):
        ruta_base = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "iconos",
            "sprites"
        )
        carpetas = ["animales", "plantas"]
        for carpeta in carpetas:
            ruta_carpeta = os.path.join(
                ruta_base, carpeta
            )
            if not os.path.isdir(ruta_carpeta):
                print("No existe:", ruta_carpeta)
                continue
            for archivo in os.listdir(ruta_carpeta):
                if archivo.lower().endswith(".png"):
                    ruta = os.path.join(
                        ruta_carpeta, archivo
                    )
                    with Image.open(ruta) as imagen:
                        self.sprites_originales[archivo] = (
                            imagen.convert("RGBA")
                        )

    def redimensionar_sprites(self):
        self.sprites.clear()
        tam = max(1, int(self.tam_celda))
        for nombre, imagen in self.sprites_originales.items():
            # Determinar tamaño según el sprite
            if nombre.startswith("michi"):
                escala = 3
            elif "semilla" in nombre:
                escala = 1
            elif "etapa1" in nombre or "brote" in nombre:
                escala = 2
            elif "etapa2" in nombre or "joven" in nombre:
                escala = 3
            elif "etapa3" in nombre or "adulta" in nombre:
                escala = 4
            else:
                escala = 1
            # Eliminar márgenes transparentes
            copia = imagen.copy()
            limites = copia.getbbox()
            if limites:
                copia = copia.crop(limites)
            # Conservar las proporciones originales
            factor = (tam * escala) / max(copia.size)
            ancho = max(1, int(copia.width * factor))
            alto = max(1, int(copia.height * factor))
            copia = copia.resize(
                (ancho, alto),
                Image.Resampling.NEAREST
            )
            self.sprites[nombre] = ImageTk.PhotoImage(
                copia,
                master=self.ventana
            )
    def obtener_sprite(self, codigo, fila, columna):
        # Animales
        if codigo == mz.ANIMAL:
            return animales.obtener_sprite(
                fila, columna
            )
        # Plantas y semillas
        sprites_plantas = {
            mz.SEMILLA: "arbol_semilla.png",
            # Árbol
            8: "arbol_etapa1.png",
            9: "arbol_etapa2.png",
            10: "arbol_etapa3.png",
            # Girasol
            12: "planta_brote.png",
            13: "planta_joven.png",
            14: "planta_adulta.png",
            # Tomatera
            15: "tomate_brote.png",
            16: "tomate_joven.png",
            17: "tomate_adulta.png"
        }
        return sprites_plantas.get(codigo)
    def crear_celdas(self):
        self.canvas.delete("all")
        self.tam_celda = TAM_CANVAS / self.n
        self.sprites_canvas.clear()
        self.redimensionar_sprites()
        self.celdas = []
        for f in range(self.n):
            fila = []
            for c in range(self.n):
                x = c * self.tam_celda
                y = f * self.tam_celda
                rectangulo = self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.tam_celda,
                    y + self.tam_celda,
                    fill=mz.COLORES[mz.AIRE],
                    outline=""
                )
                fila.append(rectangulo)
            self.celdas.append(fila)
        self.dibujado = [
            [mz.AIRE] * self.n
            for _ in range(self.n)
        ]
        self.dibujar()
    def dibujar(self):
        for f in range(self.n):
            for c in range(self.n):
                codigo = self.matriz[f][c]
                posicion = (f, c)
                nombre_sprite = self.obtener_sprite(
                    codigo, f, c
                )
# elementos que utilizan sprites (animales y plantas)
                if nombre_sprite in self.sprites:
                    imagen = self.sprites[nombre_sprite]
                    # Fondo de la celda
                    if codigo != self.dibujado[f][c]:
                        self.canvas.itemconfig(
                            self.celdas[f][c],
                            fill=mz.COLORES[mz.AIRE]
                        )
                    # Crear el sprite
                    if posicion not in self.sprites_canvas:
                        x = (c + 0.5) * self.tam_celda
                        y = (f + 1) * self.tam_celda
                        identificador = (
                            self.canvas.create_image(
                                x,
                                y,
                                image=imagen,
                                anchor="s"
                            )
                        )
                        self.sprites_canvas[posicion] = (
                            identificador
                        )
                    # Actualizar el sprite existente
                    else:
                        self.canvas.itemconfig(
                            self.sprites_canvas[posicion],
                            image=imagen
                        )
# elementos que no utilizan sprites (solo color de celda)
                else:
                    # Eliminar sprite anterior
                    if posicion in self.sprites_canvas:
                        self.canvas.delete(
                            self.sprites_canvas[posicion]
                        )
                        del self.sprites_canvas[posicion]
                    # Actualizar color de la celda
                    if codigo != self.dibujado[f][c]:
                        self.canvas.itemconfig(
                            self.celdas[f][c],
                            fill=mz.COLORES.get(
                                codigo,
                                mz.COLORES[mz.AIRE]
                            )
                        )
                self.dibujado[f][c] = codigo
        # Mantener visible la guía del rectángulo
        self.canvas.tag_raise("guia")
    def poner_matriz(self, nueva):
        """Cambia la matriz completa (al cargar o cambiar N)."""
        self.matriz = nueva
        self.n = len(nueva)
        self.entrada_n.delete(0, tk.END)
        self.entrada_n.insert(0, str(self.n))
        self.reiniciar()
        self.crear_celdas()

   # mouse
    def pixel_a_celda(self, evento):
        return int(evento.y // self.tam_celda), int(evento.x // self.tam_celda)
    
    def clic(self, evento):
        fila, col = self.pixel_a_celda(evento)
        # Verificar los límites del mapa
        if not (0 <= fila < self.n and 0 <= col < self.n):
            return
        # Animales y semillas: uno por clic
        if self.elemento in (mz.ANIMAL, mz.SEMILLA):
            if self.matriz[fila][col] == mz.AIRE:
                self.matriz[fila][col] = self.elemento
            return
        # Materiales normales
        if self.modo == "pincel":
            mz.pintar_pincel(
                self.matriz,
                fila,
                col,
                self.elemento,
                self.pincel.get()
            )
        else:
            self.inicio_rect = (fila, col)
    def arrastrar(self, evento):
        # No generar animales ni semillas al arrastrar
        if self.elemento in (mz.ANIMAL, mz.SEMILLA):
            return
        fila, col = self.pixel_a_celda(evento)
        if self.modo == "pincel":
            mz.pintar_pincel(
                self.matriz,
                fila,
                col,
                self.elemento,
                self.pincel.get()
            )
        elif self.inicio_rect:
            self.canvas.delete("guia")
            f0, c0 = self.inicio_rect
            t = self.tam_celda
            self.canvas.create_rectangle(
                min(c0, col) * t,
                min(f0, fila) * t,
                (max(c0, col) + 1) * t,
                (max(f0, fila) + 1) * t,
                outline="yellow",
                tags="guia"
            )
    def soltar(self, evento):
        if self.elemento in (mz.ANIMAL, mz.SEMILLA):
            self.inicio_rect = None
            self.canvas.delete("guia")
            return
        if self.modo == "rectangulo" and self.inicio_rect:
            fila, col = self.pixel_a_celda(evento)
            f0, c0 = self.inicio_rect
            mz.pintar_rectangulo(self.matriz, f0, c0, fila, col, self.elemento)
            self.inicio_rect = None
            self.canvas.delete("guia")

    # botones
    def elegir(self, codigo):
        self.elemento = codigo
        sonido.reproducir("clic")
        nombre = "Borrador" if codigo == mz.AIRE else mz.NOMBRES[codigo]
        self.lbl_actual.config(
            text="Actual: " + nombre
        )
        # Restaurar el diseño de todos los botones
        for clave, boton in self.botones_elementos.items():
            if clave == mz.AIRE:
                boton.config(
                    bg="#DCC28A",
                    fg="#29382B",
                    relief="flat"
                )
            else:
                boton.config(
                    bg="#263629",
                    fg="white",
                    relief="flat"
                )
        # Destacar el elemento seleccionado
        self.botones_elementos[codigo].config(
            bg="#F3D391",
            fg="#29382B",
            relief="sunken"
        )

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

    def ciclo(self):
        if not self.activo:
            return
        if not self.pausado:
            self.paso(self.matriz)
        self.dibujar()
        self.ventana.after(VELOCIDAD_MS, self.ciclo)