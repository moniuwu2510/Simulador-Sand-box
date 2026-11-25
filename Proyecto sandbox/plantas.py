import matriz as mz
import random
# Códigos de las etapas de cada especie
ARBOL = (8, 9, 10)
GIRASOL = (12, 13, 14)
TOMATE = (15, 16, 17)
ESPECIES = [ARBOL, GIRASOL, TOMATE]
# Cantidad de ticks necesarios para crecer
TIEMPO_CRECIMIENTO = 30
# Contador de tiempo de cada planta
tiempos = {}
def actualizar(matriz):
    n = len(matriz)
# gravedad: las semillas caen si debajo hay aire
    for f in range(n - 2, -1, -1):
        for c in range(n):
            if matriz[f][c] == mz.SEMILLA:
                # Caer si debajo hay aire
                if matriz[f + 1][c] == mz.AIRE:
                    matriz[f + 1][c] = mz.SEMILLA
                    matriz[f][c] = mz.AIRE
# tiempo de crecimiento: las semillas germinan y las plantas crecen
    tiempos_nuevos = {}
    for f in range(n):
        for c in range(n):
            codigo = matriz[f][c]
            posicion = (f, c)
            # Germinación de la semilla
            if codigo == mz.SEMILLA:
                # Verificar límite inferior
                if f + 1 < n:
                    # Solo germina sobre pasto
                    if matriz[f + 1][c] in (mz.PASTO, mz.TIERRA):
                        tiempo = tiempos.get(posicion, 0) + 1
                        if tiempo >= TIEMPO_CRECIMIENTO:
                            especie = random.choice(ESPECIES)
                            matriz[f][c] = especie[0]
                            tiempo = 0
                        tiempos_nuevos[posicion] = tiempo
            # Crecimiento de las plantas
            else:
                for especie in ESPECIES:
                    if codigo in especie:
                        etapa = especie.index(codigo)
                        # Si todavía puede crecer
                        if etapa < 2:
                            tiempo = tiempos.get(posicion, 0) + 1
                            if tiempo >= TIEMPO_CRECIMIENTO:
                                # Verificar espacio superior
                                if f > 0 and matriz[f - 1][c] == mz.AIRE:
                                    matriz[f][c] = especie[etapa + 1]
                                    tiempo = 0
                            tiempos_nuevos[posicion] = tiempo
                        break
    # Eliminar registros de plantas que ya no existen
    tiempos.clear()
    tiempos.update(tiempos_nuevos)
def reiniciar():
    tiempos.clear()