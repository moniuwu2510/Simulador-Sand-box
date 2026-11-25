
# mapas.py
# Guardar, cargar y limpiar mapas.
#
# Formato del archivo (.txt):
#   Línea 1: tamaño N.
#   Siguientes N líneas: códigos de los elementos.
#
# Las etapas de las plantas se guardan mediante sus códigos.

import matriz as mz


def guardar_mapa(matriz, ruta):
    """
    Guarda el tamaño y todos los elementos de la matriz.
    """

    valida, mensaje = mz.validar_matriz(matriz)

    if not valida:
        raise ValueError("No se puede guardar el mapa: " + mensaje)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(str(len(matriz)) + "\n")

        for fila in matriz:
            archivo.write(" ".join(str(x) for x in fila) + "\n")


def cargar_mapa(ruta):
    """
    Carga una matriz desde un archivo TXT.
    Comprueba que el archivo tenga un formato válido.
    Devuelve la matriz cargada.
    """

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = [linea.strip() for linea in archivo if linea.strip()]

    except OSError:
        raise OSError("No se pudo abrir el archivo del mapa.")

    if not lineas:
        raise ValueError("El archivo está vacío.")

    # Comprobar el tamaño N.
    if not lineas[0].isdigit():
        raise ValueError("La primera línea debe contener el tamaño N.")

    n = int(lineas[0])

    if not mz.validar_n(n):
        raise ValueError(
            f"El tamaño del mapa debe estar entre {mz.N_MIN} y {mz.N_MAX}."
        )

    # Comprobar la cantidad de filas.
    if len(lineas) - 1 != n:
        raise ValueError(
            f"Se esperaban {n} filas y se encontraron {len(lineas) - 1}."
        )

    matriz = []

    # Leer los códigos de cada fila.
    for i in range(1, n + 1):

        valores = lineas[i].split()

        if len(valores) != n:
            raise ValueError(
                f"La fila {i} debe contener exactamente {n} valores."
            )

        fila = []

        for valor in valores:

            if not valor.isdigit():
                raise ValueError(
                    f"Valor no numérico '{valor}' en la fila {i}."
                )

            fila.append(int(valor))

        matriz.append(fila)

    # Validar la matriz completa.
    valida, mensaje = mz.validar_matriz(matriz)

    if not valida:
        raise ValueError(mensaje)

    return matriz


def limpiar_mapa(matriz):
    """
    Convierte todas las celdas en aire.
    Los estados internos se reinician desde main.py.
    """

    mz.limpiar(matriz)
