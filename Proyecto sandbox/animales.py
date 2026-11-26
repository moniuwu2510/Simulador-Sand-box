import matriz as mz
import Elementos_de_sonido as sonido
# ================= Configuración =================

DERECHA = 1
IZQUIERDA = -1

VELOCIDAD_MOVIMIENTO = 5
TIEMPO_COMIENDO = 20
TIEMPO_MUERTO = 40

# Dimensiones aproximadas del sprite en celdas
ANCHO_ANIMAL = 3
ALTO_ANIMAL = 2

contador = 0
estados = {}

# Plantas que puede consumir el animal
PLANTAS = (
    mz.PLANTA_1,
    mz.PLANTA_2,
    mz.PLANTA_3,
    mz.GIRASOL_1,
    mz.GIRASOL_2,
    mz.GIRASOL_3,
    mz.TOMATE_1,
    mz.TOMATE_2,
    mz.TOMATE_3
)


# ================= Validaciones =================

def dentro_mapa(matriz, fila, columna):
    return mz.en_limites(matriz, fila, columna)


def espacio_libre(matriz, fila, columna):
    return mz.obtener(matriz, fila, columna) == mz.AIRE


def area_animal(fila, columna):
    """
    Devuelve las posiciones que ocupa
    aproximadamente el sprite del animal.
    """

    posiciones = []
    mitad = ANCHO_ANIMAL // 2

    for f in range(fila - ALTO_ANIMAL + 1, fila + 1):
        for c in range(columna - mitad, columna + mitad + 1):
            posiciones.append((f, c))

    return posiciones


def puede_moverse(matriz, fila, columna, nueva_fila, nueva_columna):
    """
    Comprueba que el área de destino esté libre
    de materiales y obstáculos.
    """

    for f, c in area_animal(nueva_fila, nueva_columna):

        if not dentro_mapa(matriz, f, c):
            return False

        # Ignorar la posición lógica del propio animal
        if (f, c) == (fila, columna):
            continue

        if matriz[f][c] != mz.AIRE:
            return False

    return True


# ================= Estados =================

def crear_estado():

    return {
        "direccion": DERECHA,
        "fotograma": 0,
        "accion": "quieto",
        "tiempo": 0
    }


# ================= Interacciones =================

def detectar_fuego(matriz, fila, columna):
    """
    Comprueba si existe fuego dentro o junto
    al área que ocupa el animal.
    """

    for f, c in area_animal(fila, columna):

        if mz.obtener(matriz, f, c) == mz.FUEGO:
            return True

        if mz.tiene_vecino(matriz, f, c, mz.FUEGO):
            return True

    return False


def detectar_planta(matriz, fila, columna, direccion):
    """
    Busca una planta delante del animal.
    Retorna su posición o None.
    """

    distancia = ANCHO_ANIMAL // 2 + 1

    c = columna + direccion * distancia

    for f in range(fila - ALTO_ANIMAL + 1, fila + 1):

        if mz.obtener(matriz, f, c) in PLANTAS:
            return (f, c)

    return None


def detectar_agua(matriz, fila, columna):
    """
    Comprueba si existe agua debajo del
    área que ocupará el animal.
    """

    mitad = ANCHO_ANIMAL // 2

    for c in range(columna - mitad, columna + mitad + 1):

        if mz.obtener(matriz, fila + 1, c) == mz.AGUA:
            return True

    return False


# ================= Actualización general =================

def actualizar(matriz):

    global contador

    contador += 1

    n = len(matriz)

    mover = contador >= VELOCIDAD_MOVIMIENTO

    if mover:
        contador = 0

    posiciones = []
    nuevos_estados = {}

    # Registrar los animales existentes
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

        # ================= Animal muerto =================

        if estado["accion"] == "muerto":

            estado["tiempo"] -= 1

            if estado["tiempo"] <= 0:
                matriz[f][c] = mz.AIRE
            else:
                nuevos_estados[(f, c)] = estado

            continue

        # ================= Contacto con fuego =================

        # ================= Muerte por fuego =================

        if detectar_fuego(matriz, f, c):

            estado["accion"] = "muerto"
            estado["tiempo"] = TIEMPO_MUERTO

            sonido.reproducir("muerte")

            nuevos_estados[(f, c)] = estado

            continue

        # ================= Animal comiendo =================

        if estado["accion"] == "comiendo":

            estado["tiempo"] -= 1

            if estado["tiempo"] <= 0:
                estado["accion"] = "quieto"

            nuevos_estados[(f, c)] = estado

            continue

        # ================= Gravedad =================

        if (
            espacio_libre(matriz, f + 1, c)
            and puede_moverse(matriz, f, c, f + 1, c)
            and not detectar_agua(matriz, f + 1, c)
        ):

            nueva_fila = f + 1

            estado["accion"] = "quieto"

        # ================= Movimiento horizontal =================

        elif mover:

            planta = detectar_planta(matriz, f, c, direccion)

            if planta is not None:

                pf, pc = planta

                matriz[pf][pc] = mz.AIRE

                estado["accion"] = "comiendo"
                estado["tiempo"] = TIEMPO_COMIENDO

                sonido.reproducir("comiendo")

                nuevos_estados[(f, c)] = estado

                continue

            # Calcular la siguiente posición del gato
            destino = c + direccion

            if (
                puede_moverse(matriz, f, c, f, destino)
                and not detectar_agua(matriz, f, destino)
            ):

                nueva_columna = destino
                estado["accion"] = "caminar"
                estado["fotograma"] = 1 - estado["fotograma"]

            else:

                estado["direccion"] *= -1
                estado["accion"] = "quieto"
                estado["fotograma"] = 0
        # ================= Actualizar posición =================

        if (nueva_fila, nueva_columna) != (f, c):

            mz.intercambiar(
                matriz,
                f,
                c,
                nueva_fila,
                nueva_columna
            )

        nuevos_estados[
            (nueva_fila, nueva_columna)
        ] = estado

    # Conservar únicamente los animales existentes
    estados.clear()
    estados.update(nuevos_estados)


# ================= Sprites =================

def obtener_sprite(fila, columna):

    estado = estados.get(
        (fila, columna),
        crear_estado()
    )

    if estado["accion"] == "muerto":
        return "michi_muerto.png"

    if estado["accion"] == "comiendo":
        return "michi_comiendo.png"

    if estado["direccion"] == DERECHA:
        direccion = "derecha"
    else:
        direccion = "izquierda"

    if estado["fotograma"] == 1:
        return "michi_camina_" + direccion + ".png"

    return "michi_" + direccion + ".png"
# ================= Reiniciar =================

def reiniciar():

    global contador

    contador = 0
    estados.clear()