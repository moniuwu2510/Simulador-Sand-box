import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matriz as mz
import mapas
import elementos
import interacciones
import plantas
import animales
import Elementos_de_sonido as sonido
from GUI import Juego
import os
import Elementos_de_sonido as sonido

def paso_simulacion(matriz): # inicializamos la simulación, elementos e interacciones con prioridad
    elementos.actualizar(matriz)
    interacciones.actualizar(matriz)
    plantas.actualizar(matriz)
    animales.actualizar(matriz)

def reiniciar_estados(): # reinicia estados de todo al iniciar
    elementos.reiniciar()
    interacciones.reiniciar()
    plantas.reiniciar()
    animales.reiniciar()
    
class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("MichiBox crea tu propia aventura") # cargamos atributos de la clase 
        self.root.geometry("1100x800")
        self.root.resizable(False, False)
        self.matriz = mz.crear_matriz(mz.N_DEFECTO)
        self.ventanas = {}
        self.juego = None
        self.crear_menu()
        sonido.iniciar_musica()
        # iniciamos metodos
    def crear_menu(self):
        imagen = Image.open("fondo_sandbox.png") # importamos imagen de fondo de las mismas dimensiones que la ventana
        imagen = imagen.resize((1100, 800))
        self.fondo = ImageTk.PhotoImage(
            imagen, master=self.root
        )
        self.canvas = tk.Canvas(
            self.root,
            width=1100,
            height=800,
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.create_image( # guardamos la imagen
            0, 0,
            image=self.fondo,
            anchor="nw"
        )
        imagen = Image.open("logo_sandbox.png")  # importamos logo y slogan
        imagen = imagen.resize((550, 300))

        self.logo = ImageTk.PhotoImage(
            imagen, master=self.root
        )

        self.canvas.create_image(
            775, 50,
            image=self.logo, # ubicamos logo 
            anchor="n"
        )
        
        label = tk.Label(
            self.root,
            text="Seleccione una opción",  # label de instruccion general
            font=("Segoe UI Black", 22, "bold"),
            bg="#29382B",
            fg="white"
        )

        label.place(
            x=50, y=50,
            width=400, height=60
        )
# botones del menu principal
        boton1 = tk.Button(
            self.root,
            text="Jugar",
            command=lambda: (sonido.reproducir("clic"), self.jugar()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton1.place(x=100, y=150, width=300, height=60)

        boton2 = tk.Button(
            self.root,
            text="Cargar mapa",
            command=lambda: (sonido.reproducir("clic"), self.cargar()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton2.place(x=100, y=250, width=300, height=60)

        boton3 = tk.Button(
            self.root,
            text="Guardar mapa",
            command=lambda: (sonido.reproducir("clic"), self.guardar()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton3.place(x=100, y=350, width=300, height=60)

        boton4 = tk.Button(
            self.root,
            text="Sonido",
            command=lambda: (sonido.reproducir("clic"), self.abrir_sonido()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton4.place(x=100, y=450, width=300, height=60)

        boton5 = tk.Button(
            self.root,
            text="Instrucciones",
            command=lambda: (sonido.reproducir("clic"), self.abrir_instrucciones()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton5.place(x=100, y=550, width=300, height=60)

        boton6 = tk.Button(
            self.root,
            text="Salir",
            command=lambda: (sonido.reproducir("clic"), self.salir()),
            font=("Impact", 18),
            bg="#587B40",
            fg="white",
            activebackground="#789B58",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        boton6.place(x=100, y=650, width=300, height=60)
        
        label = tk.Label(
            self.root,
            text="¡Construye tu propio mundo!", # etiqueta del juego
            font=("Segoe UI Black", 22, "bold"),
            bg="#29382B",
            fg="white"
        )
        label.place(
            x=500, y=400,
            width=550, height=60
        )
# etiqueta de descripcion del mundo del juego que puedes hacer con el entorno
        descripcion = tk.Label(
            self.root,
            text="Experimenta con los elementos.\n"
                 "Crea tus propios ecosistemas.\n"
                 "Descubre nuevas interacciones.\n"
                 "¡El límite es tu imaginación!",
            font=("Segoe UI", 18),
            bg="#29382B",
            fg="white",
            justify="center"
        )
        descripcion.place(
            x=500, y=460,
            width=550, height=200
        )
        # control de ventanas mejorado si ya existe otra no abre devuelve True
    def ventana_abierta(self, nombre):
        v = self.ventanas.get(nombre)
        if v is not None and v.winfo_exists():
            v.deiconify()
            v.lift()
            v.focus_force()
            return True
        return False
    def jugar(self):
        if self.juego is not None:
            self.ventana_abierta("juego")
            return

        self.juego = Juego(
            self.root,
            self.matriz,
            paso_simulacion,
            reiniciar_estados,
            self.al_cerrar_juego
        )

        self.ventanas["juego"] = self.juego.ventana

        # Ocultar el menú principal
        self.root.withdraw()

        # Dar prioridad a la ventana del juego
        self.juego.ventana.deiconify()
        self.juego.ventana.lift()
        self.juego.ventana.focus_force()

        # Mantenerla temporalmente en primer plano
        self.juego.ventana.attributes("-topmost", True)

        self.juego.ventana.after(
            200,
            lambda: self.juego.ventana.attributes("-topmost", False)
        )
# guardamos mundo al cerrar el juego
    def al_cerrar_juego(self, matriz):
        self.matriz = matriz
        self.juego = None

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        self.root.attributes("-topmost", True)

        self.root.after(
            200,
            lambda: self.root.attributes("-topmost", False)
        )
# cargamos mapas
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
# guardamos mapas
    def guardar(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Mapa", "*.txt")])
        if ruta:
            mapas.guardar_mapa(self.matriz, ruta)
            messagebox.showinfo("Guardado", "Mapa guardado correctamente.")
# abrimos sonidos
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

# abre las instrucciones

    def abrir_instrucciones(self):
        if self.ventana_abierta("instrucciones"):
            return
        v = tk.Toplevel(self.root)
        v.title("MichiBox | Guía del explorador")
        v.geometry("1100x800")
        v.resizable(False, False)
        v.configure(bg="#29382B")

        self.ventanas["instrucciones"] = v

        # Paleta de colores
        FONDO = "#29382B"
        PANEL = "#354B36"
        OSCURO = "#263629"
        VERDE = "#587B40"
        DORADO = "#F3D391"
        BLANCO = "#FFFFFF"
        TEXTO = "#DCE5D5"

        # Guardar referencias de las imágenes
        v.iconos = []

        ruta_iconos = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "iconos"
        )

        # ==============================
        # ENCABEZADO
        # ==============================

        encabezado = tk.Frame(v, bg=OSCURO)

        encabezado.pack(
            fill="x",
            padx=20,
            pady=(5, 5)
        )

        tk.Label(
            encabezado,
            text="MICHIBOX",
            font=("Segoe UI", 11, "bold"),
            bg=OSCURO,
            fg="#B5C99C"
        ).pack(pady=(8, 0))

        tk.Label(
            encabezado,
            text="GUÍA DEL EXPLORADOR",
            font=("Impact", 28),
            bg=OSCURO,
            fg=DORADO
        ).pack()

        tk.Label(
            encabezado,
            text="¡Aprende a construir tu propio mundo!",
            font=("Segoe UI", 11),
            bg=OSCURO,
            fg=BLANCO
        ).pack(pady=(0, 10))

        # ==============================
        # FUNCIÓN PARA CREAR SECCIONES
        # ==============================

        def crear_seccion(titulo):

            marco = tk.Frame(v, bg=PANEL)

            marco.pack(
                fill="x",
                padx=20,
                pady=5
            )

            tk.Label(
                marco,
                text=titulo,
                font=("Segoe UI Black", 14),
                bg=PANEL,
                fg=DORADO
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 5)
            )

            contenido = tk.Frame(marco, bg=PANEL)

            contenido.pack(
                fill="x",
                padx=15,
                pady=(0, 10)
            )

            return contenido

        # ==============================
        # SECCIÓN 1: CÓMO JUGAR
        # ==============================

        controles = crear_seccion("01. Cómo jugar")

        instrucciones = [
            ("Clic izquierdo",
             "Selecciona y coloca un elemento."),

            ("Arrastrar",
             "Pinta varias celdas con materiales."),

            ("Pincel",
             "Ajusta el tamaño del área de pintura."),

            ("Modo rectángulo",
             "Rellena un área completa."),

            ("Borrador",
             "Convierte las celdas en aire."),

            ("Tamaño del mundo (N)",
             "Selecciona un valor entre 20 y 100.")
        ]

        for i, (titulo, descripcion) in enumerate(instrucciones):

            tarjeta = tk.Frame(controles, bg=OSCURO)

            tarjeta.grid(
                row=i // 3,
                column=i % 3,
                padx=4,
                pady=3,
                sticky="nsew"
            )

            tk.Label(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 10, "bold"),
                bg=OSCURO,
                fg=DORADO
            ).pack(anchor="w", padx=10, pady=(4, 0))

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Segoe UI", 10),
                bg=OSCURO,
                fg=TEXTO,
                justify="left"
            ).pack(anchor="w", padx=10, pady=(0, 4))

        controles.columnconfigure(0, weight=1)
        controles.columnconfigure(1, weight=1)
        controles.columnconfigure(2, weight=1)

        # ==============================
        # SECCIÓN 2: ELEMENTOS
        # ==============================

        panel_elementos = crear_seccion(
            "02. Conoce los elementos"
        )

        lista_elementos = [
            ("Arena", "arena.png",
             "Cae y se desliza en diagonal."),

            ("Agua", "agua.png",
             "Fluye hacia los lados y se acumula."),

            ("Piedra", "piedra.png",
             "Material fijo para construir paredes."),

            ("Tierra", "tierra.png",
             "Al combinarse con agua genera pasto."),

            ("Pasto", "pasto.png",
             "Permite la germinación de semillas."),

            ("Fuego", "fuego.png",
             "Quema el pasto y se apaga con agua."),

            ("Semilla", "semilla.png",
             "Germina y crece en tres etapas."),

            ("Animal", "animal.png",
             "Camina solo y evita agua y obstáculos.")
        ]

        for i, (nombre, archivo, descripcion) in enumerate(
            lista_elementos
        ):

            tarjeta = tk.Frame(
                panel_elementos,
                bg=OSCURO
            )

            tarjeta.grid(
                row=i // 4,
                column=i % 4,
                padx=4,
                pady=3,
                sticky="nsew"
            )
            ruta = os.path.join(ruta_iconos, archivo)
            # Cargar icono si existe
            if os.path.isfile(ruta):
                with Image.open(ruta) as original:
                    imagen = original.convert("RGBA")
                    imagen = imagen.resize(
                        (36, 36),
                        Image.Resampling.NEAREST
                    )
                icono = ImageTk.PhotoImage(
                    imagen,
                    master=v
                )
                v.iconos.append(icono)
                tk.Label(
                    tarjeta,
                    image=icono,
                    bg=OSCURO
                ).pack(
                    side="left",
                    padx=8,
                    pady=5
                )
            informacion = tk.Frame(
                tarjeta,
                bg=OSCURO
            )
            informacion.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5,
                pady=4
            )

            tk.Label(
                informacion,
                text=nombre,
                font=("Segoe UI", 11, "bold"),
                bg=OSCURO,
                fg=DORADO
            ).pack(anchor="w")

            tk.Label(
                informacion,
                text=descripcion,
                font=("Segoe UI", 9),
                bg=OSCURO,
                fg=TEXTO,
                wraplength=300,
                justify="left"
            ).pack(anchor="w")

        for i in range(4):
            panel_elementos.columnconfigure(i, weight=1)

        # ==============================
        # SECCIÓN 3: MAPAS
        # ==============================

        panel_mapas = crear_seccion(
            "03. Administra tus mundos"
        )

        opciones_mapas = [
            ("Guardar", "Guarda tu mundo en un archivo .txt."),
            ("Cargar", "Recupera un mundo guardado."),
            ("Limpiar", "Convierte todo el mundo en aire.")
        ]

        for i, (titulo, descripcion) in enumerate(opciones_mapas):

            tarjeta = tk.Frame(panel_mapas, bg=OSCURO)

            tarjeta.grid(
                row=0,
                column=i,
                padx=4,
                sticky="nsew"
            )

            tk.Label(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 11, "bold"),
                bg=OSCURO,
                fg=DORADO
            ).pack(pady=(5, 0))

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Segoe UI", 9),
                bg=OSCURO,
                fg=TEXTO,
                wraplength=170,
                justify="center"
            ).pack(padx=8, pady=(0, 5))

            panel_mapas.columnconfigure(i, weight=1)

        tk.Button(
            v,
            text="VOLVER AL MENÚ",
            command=lambda: (
                sonido.reproducir("clic"),
                v.destroy()
            ),
            font=("Impact", 16),
            bg=VERDE,
            fg=BLANCO,
            activebackground="#789B58",
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2",
            width=25
        ).pack(pady=10)

        # Dar prioridad a la ventana
        v.lift()
        v.focus_force()

# salimos window destroy
    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    Menu(root)
    root.mainloop()