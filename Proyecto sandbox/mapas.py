# mapas.py
# Guardar, cargar y limpiar mapas.
#
# Formato del archivo (.txt legible):
#   línea 1: N
#   siguientes N líneas: N códigos separados por espacios
# La etapa de cada planta queda guardada porque está en su código (8, 9, 10).

import matriz as mz


def guardar_mapa(matriz, ruta):
    with open(ruta, "w") as archivo:
        archivo.write(str(len(matriz)) + "\n")
        for fila in matriz:
            archivo.write(" ".join(str(x) for x in fila) + "\n")


def cargar_mapa(ruta):
    """Devuelve la matriz del archivo. Si no es válido lanza ValueError
    con un mensaje claro (quien llama lo muestra sin cerrar el programa)."""
    with open(ruta, "r") as archivo:
        lineas = [l.strip() for l in archivo if l.strip() != ""]

    if len(lineas) == 0:
        raise ValueError("El archivo está vacío.")
    if not lineas[0].isdigit():
        raise ValueError("La primera línea debe ser el tamaño N.")
    n = int(lineas[0])
    if len(lineas) - 1 != n:
        raise ValueError(f"Se esperaban {n} filas y el archivo tiene {len(lineas) - 1}.")

    matriz = []
    for i in range(1, n + 1):
        fila = []
        for p in lineas[i].split():
            if not p.isdigit():
                raise ValueError(f"Valor no numérico '{p}' en la fila {i}.")
            fila.append(int(p))
        matriz.append(fila)

    valida, mensaje = mz.validar_matriz(matriz)
    if not valida:
        raise ValueError(mensaje)
    return matriz


def limpiar_mapa(matriz):
    """Todo a aire. Los estados internos de otros módulos se reinician en main.py."""
    mz.limpiar(matriz)