
# interacciones.py
# Colisiones y transformaciones:
# agua + tierra = pasto
# fuego + pasto = fuego (propagación)
# fuego extinguido = tierra
# agua + fuego = extinción.
#
# main.py llama a actualizar(matriz) en cada tick.

import matriz as mz
import random

# ================= Configuración del fuego =================

DURACION_FUEGO = 20
PROBABILIDAD_PROPAGACION = 0.15

# Guarda el tiempo restante de cada fuego.
# La clave es su posición (fila, columna).
tiempos_fuego = {}

# ================= Actualización general =================

def actualizar(matriz):
    """
    Revisa las interacciones entre elementos
    y actualiza la propagación y duración del fuego.
    """

    n = len(matriz)

    # Copia del estado inicial del tick.
    original = mz.copiar_matriz(matriz)

    # Identificar las posiciones que contienen fuego.
    posiciones_fuego = []

    for f in range(n):
        for c in range(n):
            if original[f][c] == mz.FUEGO:
                posiciones_fuego.append((f, c))

    # Registrar fuegos nuevos y eliminar estados antiguos.
    posiciones_actuales = set(posiciones_fuego)

    for posicion in posiciones_fuego:
        if posicion not in tiempos_fuego:
            tiempos_fuego[posicion] = DURACION_FUEGO

    for posicion in list(tiempos_fuego):
        if posicion not in posiciones_actuales:
            del tiempos_fuego[posicion]

    # 1. Agua transforma tierra en pasto.
    for f in range(n):
        for c in range(n):

            if original[f][c] == mz.TIERRA:
                if tiene_vecino_en(original, f, c, mz.AGUA):
                    matriz[f][c] = mz.PASTO

    # 2. Actualizar los fuegos existentes.
    for f, c in posiciones_fuego:

        # Comprobar que el fuego siga existiendo.
        if matriz[f][c] != mz.FUEGO:
            continue

        # El agua extingue el fuego.
        if tiene_vecino_en(original, f, c, mz.AGUA):
            matriz[f][c] = mz.AIRE
            tiempos_fuego.pop((f, c), None)
            continue

        # Reducir el tiempo de vida.
        tiempos_fuego[(f, c)] -= 1

        # Si termina su duración, se convierte en tierra.
        if tiempos_fuego[(f, c)] <= 0:
            matriz[f][c] = mz.TIERRA
            tiempos_fuego.pop((f, c), None)
            continue

        # 3. Intentar propagar el fuego.
        if random.random() < PROBABILIDAD_PROPAGACION:

            pastos = []

            for nf, nc in mz.vecinos(original, f, c):

                if (
                    original[nf][nc] == mz.PASTO
                    and matriz[nf][nc] == mz.PASTO
                ):
                    pastos.append((nf, nc))

            # Propagar hacia un pasto aleatorio.
            if pastos:
                nf, nc = random.choice(pastos)

                matriz[nf][nc] = mz.FUEGO
                tiempos_fuego[(nf, nc)] = DURACION_FUEGO

# ================= Comprobación de vecinos =================

def tiene_vecino_en(matriz, fila, col, codigo):
    """
    Comprueba si existe un elemento determinado
    arriba, abajo, a la izquierda o a la derecha.
    """

    for f, c in mz.vecinos(matriz, fila, col):
        if matriz[f][c] == codigo:
            return True

    return False

# ================= Reiniciar =================

def reiniciar():
    """
    Elimina todos los contadores de duración del fuego.
    """

    tiempos_fuego.clear()
