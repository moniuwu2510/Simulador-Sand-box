import pygame
# Inicialización del sistema de sonido
if not pygame.mixer.get_init():
    pygame.mixer.init()
# Estado de los efectos de sonido
activado = True
volumen = 70
# Carga de archivos de sonido
sonido_boton = pygame.mixer.Sound("boton_efecto.mp3")
sonido_boton.set_volume(volumen / 100)
# Diccionario de sonidos disponibles
sonidos = {
    "clic": sonido_boton
}
# Activar o desactivar sonidos
def activar(valor):
    global activado
    activado = valor
# Modificar el volumen de los sonidos
def cambiar_volumen(valor):
    global volumen
    volumen = int(valor)
    for sonido in sonidos.values():
        sonido.set_volume(volumen / 100)
# Reproducir un efecto de sonido
def reproducir(nombre):
    if not activado or volumen == 0:
        return
    if nombre in sonidos:
        sonidos[nombre].play()
