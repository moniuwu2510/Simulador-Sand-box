import matriz as mz
# varoiables globales
DERECHA = 1
IZQUIERDA = -1
# Frecuencia de movimiento en ticks
VELOCIDAD_MOVIMIENTO = 5
# Contador general
contador = 0
# Estados individuales de los animales
estados = {}
# validaciones
def dentro_mapa(matriz, fila, columna):
    n = len(matriz)
    return 0 <= fila < n and 0 <= columna < n
def espacio_libre(matriz, fila, columna):
    if not dentro_mapa(matriz, fila, columna):
        return False
    return matriz[fila][columna] == mz.AIRE
# inicializamos el estado de cada animal con dirección, fotograma y acción
def crear_estado():

    return {
        "direccion": DERECHA,
        "fotograma": 0,
        "accion": "quieto"
    }
def actualizar(matriz):
    global contador
    contador += 1
    n = len(matriz)
    mover = contador >= VELOCIDAD_MOVIMIENTO
    if mover:
        contador = 0
    posiciones = []
    nuevos_estados = {}
    # Registrar las posiciones actuales
    for f in range(n):
        for c in range(n):

            if matriz[f][c] == mz.ANIMAL:
                posiciones.append((f, c))
    # Actualizar cada animal
    for f, c in posiciones:
        if matriz[f][c] != mz.ANIMAL:
            continue
        estado = estados.get((f, c), crear_estado())
        direccion = estado["direccion"]
        nueva_fila = f
        nueva_columna = c
        estado["accion"] = "quieto"
# gravedad: caer si hay aire debajo
        if espacio_libre(matriz, f + 1, c):
            nueva_fila = f + 1
# movimiento horizontal
        elif mover:
            destino = c + direccion
            if espacio_libre(matriz, f, destino):
                # Evitar caer directamente al agua
                hay_agua = (
                    dentro_mapa(matriz, f + 1, destino)
                    and matriz[f + 1][destino] == mz.AGUA
                )
                if not hay_agua:
                    nueva_columna = destino
                    estado["accion"] = "caminar"
                    estado["fotograma"] = (
                        1 - estado["fotograma"]
                    )
                else:
                    estado["direccion"] *= -1
            else:
                # Cambiar dirección ante obstáculos
                # o límites del mapa
                estado["direccion"] *= -1
# actualizar la matriz y los estados
        if (nueva_fila, nueva_columna) != (f, c):
            matriz[f][c] = mz.AIRE
            matriz[nueva_fila][nueva_columna] = mz.ANIMAL
        nuevos_estados[
            (nueva_fila, nueva_columna)
        ] = estado
    # Conservar únicamente animales existentes
    estados.clear()
    estados.update(nuevos_estados)
def obtener_sprite(fila, columna):
    estado = estados.get(
        (fila, columna),
        crear_estado()
    )
    if estado["direccion"] == DERECHA:
        direccion = "derecha"
    else:
        direccion = "izquierda"
    if estado["fotograma"] == 1:
        return "michi_camina_" + direccion + ".png"
    return "michi_" + direccion + ".png"
def reiniciar():
    global contador
    contador = 0
    estados.clear()
