
# matriz.py
# Creación y validación del mundo.
# Todo lo relacionado con la matriz: códigos, creación,
# límites, edición y validación.

# ================= Códigos de los elementos =================

AIRE = 0
ARENA = 1
AGUA = 2
PIEDRA = 3
TIERRA = 4
FUEGO = 5
SEMILLA = 6
PASTO = 7
PLANTA_1 = 8
PLANTA_2 = 9
PLANTA_3 = 10
ANIMAL = 11

NOMBRES = {
    AIRE: "Aire", ARENA: "Arena", AGUA: "Agua", PIEDRA: "Piedra",
    TIERRA: "Tierra", FUEGO: "Fuego", SEMILLA: "Semilla", PASTO: "Pasto",
    PLANTA_1: "Planta 1", PLANTA_2: "Planta 2", PLANTA_3: "Planta 3",
    ANIMAL: "Animal",
}

COLORES = {
    AIRE: "#000000", ARENA: "#e6c86e", AGUA: "#2f6fdf", PIEDRA: "#7a7a7a",
    TIERRA: "#7b4a22", FUEGO: "#ff5a00", SEMILLA: "#c9a15b", PASTO: "#3fbf3f",
    PLANTA_1: "#9be37a", PLANTA_2: "#4caf50", PLANTA_3: "#1b5e20",
    ANIMAL: "#ffffff",
}

# Elementos que el usuario puede elegir en la interfaz
SELECCIONABLES = [ARENA, AGUA, PIEDRA, TIERRA, FUEGO, SEMILLA, ANIMAL]

# Tamaño permitido del mundo.
N_MIN = 20
N_MAX = 100
N_DEFECTO = 50

# ================= Creación =================

def crear_matriz(n):
    """
    Crea una matriz cuadrada de tamaño N x N.
    Parámetros:
        n: dimensión de la matriz.
    Retorna:
        Una matriz llena de casillas de aire.
    Se valida el tamaño antes de crear la matriz.
    Si el tamaño no es válido, se genera un error.
    """

    if not validar_n(n):
        raise ValueError(
            f"N debe ser un entero entre {N_MIN} y {N_MAX}."
        )

    matriz = []

    for f in range(n):
        fila = []

        for c in range(n):
            fila.append(AIRE)

        matriz.append(fila)

    return matriz


def copiar_matriz(matriz):
    """
    Crea una copia independiente de la matriz.
    Parámetros:
        matriz: matriz que se desea copiar.
    Retorna:
        Una nueva matriz con los mismos valores.
    Se utiliza para conservar una copia del mundo sin modificar accidentalmente la matriz original.
    """

    return [fila[:] for fila in matriz]


def limpiar(matriz):
    """Convierte todas las casillas en el mundo creado en aire."""

    for f in range(len(matriz)):
        for c in range(len(matriz)):
            matriz[f][c] = AIRE


# ================= Validación =================

def validar_n(n):
    """
    Comprueba si el tamaño N es válido.
    Condiciones:
        - Debe ser un número entero.
        - Debe ser mayor o igual a 20.
        - Debe ser menor o igual a 100.
    Se utiliza type(n) == int para impedir que valores booleanos sean aceptados como dimensiones.
    """

    return type(n) == int and N_MIN <= n <= N_MAX


def es_codigo_valido(codigo):
    """Comprueba que el código corresponda a un elemento definido."""

    return type(codigo) == int and codigo in NOMBRES


def validar_matriz(matriz):
    """
    Comprueba que la matriz:
    - No esté vacía.
    - Tenga dimensiones válidas.
    - Sea cuadrada.
    - Contenga únicamente códigos válidos.

    Devuelve (True, "") si es correcta.
    Devuelve (False, mensaje) si contiene errores.
    """

    if type(matriz) != list or len(matriz) == 0:
        return False, "La matriz está vacía o no es válida."

    n = len(matriz)

    if not validar_n(n):
        return False, (
            f"N = {n} no está entre {N_MIN} y {N_MAX}."
        )

    for i in range(n):

        if type(matriz[i]) != list or len(matriz[i]) != n:
            return False, (
                f"La fila {i + 1} no tiene {n} valores."
            )

        for valor in matriz[i]:

            if not es_codigo_valido(valor):
                return False, (
                    f"Código inválido '{valor}' "
                    f"en la fila {i + 1}."
                )

    return True, ""


def en_limites(matriz, fila, col):
    """Comprueba si una coordenada pertenece al mundo."""

    if type(fila) != int or type(col) != int:
        return False

    n = len(matriz)

    return 0 <= fila < n and 0 <= col < n


# ================= Acceso seguro =================

def obtener(matriz, fila, col):
    """
    Obtiene el contenido de una casilla.

    Si está fuera de la matriz devuelve PIEDRA,
    simulando una pared en los bordes.
    """

    if en_limites(matriz, fila, col):
        return matriz[fila][col]

    return PIEDRA


def poner(matriz, fila, col, codigo):
    """Coloca un elemento si la posición existe."""

    if not es_codigo_valido(codigo):
        raise ValueError(f"Código de elemento inválido: {codigo}")

    if en_limites(matriz, fila, col):
        matriz[fila][col] = codigo


def intercambiar(matriz, f1, c1, f2, c2):
    """Intercambia el contenido de dos casillas válidas."""

    if not en_limites(matriz, f1, c1):
        return False

    if not en_limites(matriz, f2, c2):
        return False

    matriz[f1][c1], matriz[f2][c2] = (
        matriz[f2][c2],
        matriz[f1][c1]
    )

    return True


# ================= Vecinos =================

def vecinos(matriz, fila, col):
    """Devuelve las coordenadas de las cuatro casillas vecinas."""

    resultado = []

    direcciones = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for df, dc in direcciones:

        f = fila + df
        c = col + dc

        if en_limites(matriz, f, c):
            resultado.append((f, c))

    return resultado


def tiene_vecino(matriz, fila, col, codigo):
    """Comprueba si existe un vecino con determinado código."""

    for f, c in vecinos(matriz, fila, col):

        if matriz[f][c] == codigo:
            return True

    return False


# ================= Herramientas de edición =================

def pintar_pincel(matriz, fila, col, codigo, tam_pincel):
    """
    Pinta un área cuadrada de tam_pincel x tam_pincel.

    Las posiciones que quedan fuera del mundo se ignoran.
    """

    if not es_codigo_valido(codigo):
        raise ValueError("El código del elemento no es válido.")

    if type(tam_pincel) != int or tam_pincel < 1:
        raise ValueError("El tamaño del pincel debe ser positivo.")

    if type(fila) != int or type(col) != int:
        raise ValueError("Las coordenadas deben ser enteros.")

    mitad = tam_pincel // 2

    for f in range(
        fila - mitad,
        fila - mitad + tam_pincel
    ):

        for c in range(
            col - mitad,
            col - mitad + tam_pincel
        ):

            poner(matriz, f, c, codigo)


def pintar_rectangulo(matriz, f1, c1, f2, c2, codigo):
    """
    Llena un área rectangular entre dos coordenadas.

    Permite seleccionar las esquinas en cualquier orden.
    """

    if not es_codigo_valido(codigo):
        raise ValueError("El código del elemento no es válido.")

    if any(type(x) != int for x in (f1, c1, f2, c2)):
        raise ValueError("Las coordenadas deben ser enteros.")

    fila_inicio = min(f1, f2)
    fila_final = max(f1, f2)

    col_inicio = min(c1, c2)
    col_final = max(c1, c2)

    for f in range(fila_inicio, fila_final + 1):

        for c in range(col_inicio, col_final + 1):

            poner(matriz, f, c, codigo)
