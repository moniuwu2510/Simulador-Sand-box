import matriz as mz
import random

# ================= Configuración =================

# Códigos de las etapas de cada especie
ARBOL = (
    mz.PLANTA_1,
    mz.PLANTA_2,
    mz.PLANTA_3
)

GIRASOL = (
    mz.GIRASOL_1,
    mz.GIRASOL_2,
    mz.GIRASOL_3
)

TOMATE = (
    mz.TOMATE_1,
    mz.TOMATE_2,
    mz.TOMATE_3
)

ESPECIES = [ARBOL, GIRASOL, TOMATE]

# Cantidad de ticks necesarios para crecer
TIEMPO_CRECIMIENTO = 30

# Tamaño máximo de cada etapa en celdas
TAMANOS_ETAPAS = {
    0: 2,
    1: 3,
    2: 4
}

# Contador de tiempo de cada planta
tiempos = {}


# ================= Validaciones =================

def espacio_para_crecer(matriz, fila, columna, etapa):
    """
    Comprueba si existe suficiente espacio
    para alcanzar una determinada etapa.
    """

    tam = TAMANOS_ETAPAS[etapa]

    fila_inicio = fila - tam + 1

    # Comprobar las columnas cubiertas por el sprite
    mitad = tam // 2

    columna_inicio = columna - mitad
    columna_final = columna + mitad

    for f in range(fila_inicio, fila + 1):

        for c in range(
            columna_inicio,
            columna_final + 1
        ):

            # Ignorar la posición de la propia planta
            if (f, c) == (fila, columna):
                continue

            # Comprobar límites del mundo
            if not mz.en_limites(matriz, f, c):
                return False

            # Comprobar obstáculos
            if mz.obtener(matriz, f, c) != mz.AIRE:
                return False

    return True


# ================= Gravedad =================

def mover_semillas(matriz):

    n = len(matriz)

    for f in range(n - 2, -1, -1):

        for c in range(n):

            if matriz[f][c] == mz.SEMILLA:

                if mz.obtener(matriz, f + 1, c) == mz.AIRE:

                    mz.intercambiar(
                        matriz,
                        f,
                        c,
                        f + 1,
                        c
                    )


# ================= Actualización general =================

def actualizar(matriz):

    n = len(matriz)

    # Aplicar gravedad a las semillas
    mover_semillas(matriz)

    tiempos_nuevos = {}

    for f in range(n):

        for c in range(n):

            codigo = matriz[f][c]
            posicion = (f, c)

            # ================= Germinación =================

            if codigo == mz.SEMILLA:

                # Solo germina sobre pasto
                if mz.obtener(matriz, f + 1, c) == mz.PASTO:

                    tiempo = tiempos.get(posicion, 0) + 1

                    if tiempo >= TIEMPO_CRECIMIENTO:

                        # Comprobar espacio para germinar
                        if espacio_para_crecer(matriz, f, c, 0):

                            especie = random.choice(ESPECIES)

                            matriz[f][c] = especie[0]

                            tiempo = 0

                        else:

                            tiempo = TIEMPO_CRECIMIENTO

                    tiempos_nuevos[posicion] = tiempo

            # ================= Crecimiento =================

            else:

                for especie in ESPECIES:

                    if codigo in especie:

                        etapa = especie.index(codigo)

                        # Verificar si todavía puede crecer
                        if etapa < 2:

                            tiempo = tiempos.get(posicion, 0) + 1

                            if tiempo >= TIEMPO_CRECIMIENTO:

                                siguiente_etapa = etapa + 1

                                # Comprobar espacio para crecer
                                if espacio_para_crecer(
                                    matriz,
                                    f,
                                    c,
                                    siguiente_etapa
                                ):

                                    matriz[f][c] = especie[
                                        siguiente_etapa
                                    ]

                                    tiempo = 0

                                else:

                                    # Mantener la etapa actual
                                    tiempo = TIEMPO_CRECIMIENTO

                            tiempos_nuevos[posicion] = tiempo

                        break

    # Eliminar registros de plantas que ya no existen
    tiempos.clear()
    tiempos.update(tiempos_nuevos)


# ================= Reiniciar =================

def reiniciar():

    tiempos.clear()