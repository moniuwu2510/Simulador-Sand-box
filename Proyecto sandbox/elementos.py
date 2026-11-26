"""Actualización física de los materiales móviles, principalmente arena y agua."""

# elementos.py
# Movimiento de arena y agua.
# Piedra y tierra permanecen fijas.
# El comportamiento del fuego se maneja en interacciones.py.
# main.py llama a actualizar(matriz) en cada tick.

import random
import matriz as mz

# ================= Actualización general =================

def actualizar(matriz):
    """Aplica las reglas de actualización del módulo sobre la matriz del mundo."""
    n = len(matriz)
    movido = [[False] * n for _ in range(n)]   # para no mover algo 2 veces en el mismo tick
    #De ABAJO hacia ARRIBA: lo que cae no se vuelve a procesar en este tick
    for f in range(n - 1, -1, -1):
        columnas = list(range(n))
        random.shuffle(columnas)               # evita que todo se cargue a un lado
        for c in columnas:
            if movido[f][c]:
                continue
            codigo = matriz[f][c]
            if codigo == mz.ARENA:
                mover_arena(matriz, f, c, movido)
            elif codigo == mz.AGUA:
                mover_agua(matriz, f, c, movido)

# ================= Movimiento de arena =================

def mover_arena(matriz, f, c, movido):
    """Calcula el movimiento de una partícula de arena durante un ciclo."""
    # 1. Intentar caer verticalmente.
    if mz.obtener(matriz, f + 1, c) == mz.AIRE:

        mz.intercambiar(matriz, f, c, f + 1, c)

        movido[f + 1][c] = True
        return

    # 2. Intentar caer diagonalmente.
    lados = [-1, 1]
    random.shuffle(lados)

    for d in lados:

        diagonal_libre = (
            mz.obtener(matriz, f + 1, c + d) == mz.AIRE
        )

        lado_libre = (
            mz.obtener(matriz, f, c + d) == mz.AIRE
        )

        if diagonal_libre and lado_libre:

            mz.intercambiar(matriz, f, c, f + 1, c + d)

            movido[f + 1][c + d] = True
            return


# ================= Movimiento de agua =================

def mover_agua(matriz, f, c, movido):
    """Calcula el movimiento de una partícula de agua durante un ciclo."""
    # 1. Intentar caer verticalmente.
    if mz.obtener(matriz, f + 1, c) == mz.AIRE:
        mz.intercambiar(matriz, f, c, f + 1, c)
        movido[f + 1][c] = True
        return

    # 2. Intentar caer diagonalmente.
    lados = [-1, 1]
    random.shuffle(lados)

    for d in lados:
        if (
            mz.obtener(matriz, f + 1, c + d) == mz.AIRE
            and mz.obtener(matriz, f, c + d) == mz.AIRE
        ):
            mz.intercambiar(matriz, f, c, f + 1, c + d)
            movido[f + 1][c + d] = True
            return

    # 3. Intentar desplazarse lateralmente.
    for d in lados:
        if mz.obtener(matriz, f, c + d) == mz.AIRE:
            mz.intercambiar(matriz, f, c, f, c + d)
            movido[f][c + d] = True
            return

# ================= Reiniciar =================

def reiniciar():
    """
    Reinicia los estados internos del módulo.

    Actualmente no se almacenan estados adicionales aquí.
    """
    return None
