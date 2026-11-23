# elementos.py
# Movimiento de arena, agua, tierra y fuego.
# main.py llama a actualizar(matriz) en cada tick de la simulación.

import random
import matriz as mz


def actualizar(matriz):
    n = len(matriz)
    movido = [[False] * n for _ in range(n)]   # para no mover algo 2 veces en el mismo tick
    # De ABAJO hacia ARRIBA: lo que cae no se vuelve a procesar en este tick
    for f in range(n - 1, -1, -1):
        columnas = list(range(n))
        random.shuffle(columnas)               # evita que todo se cargue a un lado
        for c in columnas:
            if movido[f][c]:
                continue
            codigo = matriz[f][c]
            if codigo == mz.ARENA:
                mover_arena(matriz, f, c, movido)
            # elif codigo == mz.AGUA:  mover_agua(matriz, f, c, movido)
            # elif codigo == mz.FUEGO: actualizar_fuego(matriz, f, c, movido)


def mover_arena(matriz, f, c, movido):
    # 1) caer recto
    if mz.obtener(matriz, f + 1, c) == mz.AIRE:
        mz.intercambiar(matriz, f, c, f + 1, c)
        movido[f + 1][c] = True
        return
    # 2) si hay obstáculo, probar en diagonal
    lados = [-1, 1]
    random.shuffle(lados)
    for d in lados:
        if mz.obtener(matriz, f + 1, c + d) == mz.AIRE and mz.obtener(matriz, f, c + d) == mz.AIRE:
            mz.intercambiar(matriz, f, c, f + 1, c + d)
            movido[f + 1][c + d] = True
            return


def reiniciar():
    """Reinicia estados internos (ej. vida del fuego) cuando se limpia el mapa."""
    pass
