import pygame
import os

# ================= Configuración inicial =================

activado = True
volumen = 70

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

try:
    pygame.mixer.init()
except pygame.error as error:
    print("No se pudo iniciar el audio:", error)


# ================= Cargar efectos =================

def cargar_sonido(nombre):

    ruta = os.path.join(RUTA_BASE, nombre)

    if not pygame.mixer.get_init():
        return None

    if os.path.isfile(ruta):
        try:
            return pygame.mixer.Sound(ruta)
        except pygame.error as error:
            print("Error al cargar sonido:", error)

    return None


sonido_boton = cargar_sonido("boton_efecto.mp3")
sonido_muerte = cargar_sonido("muerte.mp3")
sonido_comiendo = cargar_sonido("comiendo.mp3")

sonidos = {
    "clic": sonido_boton,
    "muerte": sonido_muerte,
    "comiendo": sonido_comiendo
}
# ================= Música de fondo =================

musica_cargada = False

ruta_musica = os.path.join(
    RUTA_BASE,
    "fondo_musica.mp3"
)

if pygame.mixer.get_init() and os.path.isfile(ruta_musica):

    try:
        pygame.mixer.music.load(ruta_musica)
        musica_cargada = True

    except pygame.error as error:
        print("Error al cargar música:", error)


# ================= Reproducir música =================

def iniciar_musica():

    if activado and musica_cargada:

        pygame.mixer.music.set_volume(volumen / 100)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)


def detener_musica():

    if musica_cargada:
        pygame.mixer.music.stop()


# ================= Activar y desactivar =================

def activar(estado):

    global activado

    activado = bool(estado)

    if activado:
        iniciar_musica()

    else:
        detener_musica()

        if pygame.mixer.get_init():
            pygame.mixer.stop()


# ================= Control de volumen =================

def cambiar_volumen(nuevo_volumen):

    global volumen

    volumen = max(0, min(100, float(nuevo_volumen)))

    if musica_cargada:
        pygame.mixer.music.set_volume(volumen / 100)

    for efecto in sonidos.values():

        if efecto is not None:
            efecto.set_volume(volumen / 100)


# ================= Reproducir efectos =================

def reproducir(nombre):

    if not activado:
        return

    efecto = sonidos.get(nombre)

    if efecto is not None:

        efecto.set_volume(volumen / 100)
        efecto.play()