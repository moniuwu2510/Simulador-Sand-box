# Elementos_de_sonido.py
# Sonidos del juego. Por ahora solo guarda el estado (activado y volumen)
# para que el menú de sonido funcione. Después pueden reproducir sonidos
# de verdad, por ejemplo con pygame.mixer (pip install pygame).

activado = True
volumen = 70      # 0 a 100


def activar(valor):
    global activado
    activado = valor


def cambiar_volumen(valor):
    global volumen
    volumen = int(valor)


def reproducir(nombre):
    """Llamar desde cualquier parte: reproducir("fuego"), reproducir("clic")..."""
    if not activado or volumen == 0:
        return
    # TODO: cargar y reproducir el archivo de sonido correspondiente a 'nombre'
    pass
