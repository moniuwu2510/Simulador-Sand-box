# matriz.py
# Creación y validación del mundo.
# Todo lo que tiene que ver con LA MATRIZ: códigos, crearla, revisar límites,
# pintar sobre ella y validar que una matriz sea correcta.
# Este archivo NO usa Tkinter: cualquier otro módulo lo puede importar.

# ================= Códigos de los elementos =================
AIRE = 0
ARENA = 1
AGUA = 2
PIEDRA = 3
TIERRA = 4
FUEGO = 5
SEMILLA = 6
PASTO = 7          # se genera por interacción, no se puede seleccionar
PLANTA_1 = 8
PLANTA_2 = 9
PLANTA_3 = 10
ANIMAL = 11
# Si agregan códigos nuevos (ej. fuego débil = 12), agréguenlos aquí,
# en NOMBRES y en COLORES, y documéntenlos.

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

N_MIN = 20
N_MAX = 100
N_DEFECTO = 50

# ================= Creación =================
def crear_matriz(n):
    if not validar_n(n):
        raise ValueError(f"N debe ser un entero entre {N_MIN} y {N_MAX}.")
    matriz = []
    for _ in range(n):
        fila = []
        for _ in range(n):
            fila.append(AIRE)
        matriz.append(fila)
    return matriz
"""
Crea una matriz cuadrada de tamaño N x N.
Parámetros:
    n: dimensión de la matriz.
Retorna:
    Una matriz llena de casillas de aire.
Se valida el tamaño antes de crear la matriz.
Si el tamaño no es válido, se genera un error.
"""

def copiar_matriz(matriz):
    return [fila[:] for fila in matriz]
"""
Crea una copia independiente de la matriz.
Parámetros:
    matriz: matriz que se desea copiar.
Retorna:
    Una nueva matriz con los mismos valores.
Se utiliza para conservar una copia del mundo sin modificar accidentalmente la matriz original.
"""

def limpiar(matriz):
    n = len(matriz)
    for f in range(n):
        for c in range(n):
            matriz[f][c] = AIRE
"""
Pone todas las casillas en aire (sin crear una matriz nueva).
"""

# ================= Validación =================
def validar_n(n):
    return type(n) == int and N_MIN <= n <= N_MAX
"""
Comprueba si el tamaño N es válido.
Condiciones:
    - Debe ser un número entero.
    - Debe ser mayor o igual a 20.
    - Debe ser menor o igual a 100.
    Se utiliza type(n) == int para impedir que
        valores booleanos sean aceptados como dimensiones.
"""

def es_codigo_valido(codigo):
    return type(codigo) == int and codigo in NOMBRES
"""
Comprueba si un código corresponde a un elemento definido.
Parámetros:
    codigo: número que identifica un elemento.
Retorna:
    True si el código existe.
    False si el código no está definido.
Esta validación evita introducir códigos inexistentes en la matriz.
"""

def validar_matriz(matriz):
    if type(matriz) != list or len(matriz) == 0:
        return False, "La matriz está vacía."
    n = len(matriz)
    if not validar_n(n):
        return False, f"N = {n} no está entre {N_MIN} y {N_MAX}."
    for i in range(n):
        if type(matriz[i]) != list or len(matriz[i]) != n:
            return False, f"La fila {i + 1} no tiene {n} valores (la matriz debe ser cuadrada)."
        for valor in matriz[i]:
            if not es_codigo_valido(valor):
                return False, f"Código inválido '{valor}' en la fila {i + 1}."
    return True, ""
"""
Comprueba que una matriz tenga una estructura válida.
Verifica:
    1. Que sea una lista.
    2. Que no esté vacía.
    3. Que tenga un tamaño permitido.
    4. Que todas las filas tengan la misma longitud.
    5. Que todos sus valores sean códigos válidos.
Parámetros:
    matriz: matriz que se desea comprobar.
Retorna:
    (True, "") si la matriz es válida.
    (False, mensaje) si encuentra algún error.
Se amplía la validación para detectar matrices incompletas, dimensiones incorrectas y códigos inválidos.
Esta función también será utilizada por mapas.py al cargar archivos.
    """

def en_limites(matriz, fila, col):
    """True si (fila, col) está dentro de la matriz."""
    n = len(matriz)
    return 0 <= fila < n and 0 <= col < n
"""
Comprueba si una posición se encuentra dentro del mundo.
Parámetros:
    fila: coordenada vertical.
    col: coordenada horizontal.
Retorna:
    True si la posición existe.
    False si está fuera de la matriz.
Se verifica que las coordenadas sean enteros antes de realizar las comparaciones.
"""

# ================= Acceso seguro =================
def obtener(matriz, fila, col):
    """Devuelve el código de la casilla. Fuera de la matriz devuelve PIEDRA,
    así los bordes se comportan como paredes y nadie se sale."""
    if en_limites(matriz, fila, col):
        return matriz[fila][col]
    return PIEDRA


def poner(matriz, fila, col, codigo):
    """Pone un código solo si la casilla existe."""
    if en_limites(matriz, fila, col):
        matriz[fila][col] = codigo


def intercambiar(matriz, f1, c1, f2, c2):
    """Intercambia dos casillas (así 'cae' la arena: se cambia con el aire de abajo)."""
    matriz[f1][c1], matriz[f2][c2] = matriz[f2][c2], matriz[f1][c1]


def vecinos(matriz, fila, col):
    """Lista de (f, c) de las 4 casillas vecinas que existen."""
    resultado = []
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        f, c = fila + df, col + dc
        if en_limites(matriz, f, c):
            resultado.append((f, c))
    return resultado


def tiene_vecino(matriz, fila, col, codigo):
    """True si alguna de las 4 vecinas tiene ese código (ej. tierra tocando agua)."""
    for f, c in vecinos(matriz, fila, col):
        if matriz[f][c] == codigo:
            return True
    return False


# ================= Herramientas de edición =================
def pintar_pincel(matriz, fila, col, codigo, tam_pincel):
    """Pinta un cuadrado de tam_pincel x tam_pincel centrado en (fila, col).
    Lo que se sale de la matriz se ignora."""
    mitad = tam_pincel // 2
    for f in range(fila - mitad, fila - mitad + tam_pincel):
        for c in range(col - mitad, col - mitad + tam_pincel):
            poner(matriz, f, c, codigo)


def pintar_rectangulo(matriz, f1, c1, f2, c2, codigo):
    """Llena el rectángulo entre dos esquinas (en cualquier orden)."""
    for f in range(min(f1, f2), max(f1, f2) + 1):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            poner(matriz, f, c, codigo)
