# interacciones.py
# Colisiones y transformaciones:
# agua + tierra = pasto
# fuego + pasto = tierra
# agua + fuego = extinción del fuego.
# main.py llama a actualizar(matriz) en cada tick.

import matriz as mz


# ================= Actualización general =================

def actualizar(matriz):
    """
    Revisa las interacciones entre elementos
    y aplica las transformaciones correspondientes.
    """

    n = len(matriz)

    # Se recorre una copia para evitar que las transformaciones
    # recién realizadas provoquen nuevas interacciones en el mismo tick.
    original = mz.copiar_matriz(matriz)

    for f in range(n):
        for c in range(n):

            codigo = original[f][c]

            # Agua transforma tierra en pasto.
            if codigo == mz.TIERRA:
                if tiene_vecino_en(original, f, c, mz.AGUA):
                    matriz[f][c] = mz.PASTO

            # Agua extingue el fuego.
            elif codigo == mz.FUEGO:
                if tiene_vecino_en(original, f, c, mz.AGUA):
                    matriz[f][c] = mz.AIRE

            # Fuego transforma pasto en tierra.
            elif codigo == mz.PASTO:
                if tiene_vecino_en(original, f, c, mz.FUEGO):
                    matriz[f][c] = mz.TIERRA

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
    """No hay estados internos que reiniciar actualmente."""
    pass
