from fastapi import FastAPI
from math import sqrt

app = FastAPI()

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }

# =========================================================
# CALCULAR DISTANCIA
# =========================================================
def calcular_distancia(lat1, lng1, lat2, lng2):

    return sqrt(
        (lat2 - lat1) ** 2 +
        (lng2 - lng1) ** 2
    )

# =========================================================
# OBTENER CLIENTE MÁS LEJANO
# =========================================================
def obtener_cliente_mas_lejano(origin_lat, origin_lng, clientes):

    cliente_mas_lejano = None
    distancia_maxima = -1

    for cliente in clientes:

        distancia = calcular_distancia(
            origin_lat,
            origin_lng,
            cliente["lat"],
            cliente["lng"]
        )

        if distancia > distancia_maxima:

            distancia_maxima = distancia
            cliente_mas_lejano = cliente

    return cliente_mas_lejano

# =========================================================
# ORDENAR CLIENTES POR CERCANÍA
# =========================================================
def optimizar_ruta(origin_lat, origin_lng, clientes, destination):

    clientes_restantes = clientes.copy()

    ruta_optimizada = []

    lat_actual = origin_lat
    lng_actual = origin_lng

    while clientes_restantes:

        cliente_mas_cercano = None
        distancia_minima = float("inf")

        for cliente in clientes_restantes:

            # evitar destination
            if cliente == destination:
                continue

            distancia = calcular_distancia(
                lat_actual,
                lng_actual,
                cliente["lat"],
                cliente["lng"]
            )

            if distancia < distancia_minima:

                distancia_minima = distancia
                cliente_mas_cercano = cliente

        if cliente_mas_cercano is None:
            break

        ruta_optimizada.append(cliente_mas_cercano)

        lat_actual = cliente_mas_cercano["lat"]
        lng_actual = cliente_mas_cercano["lng"]

        clientes_restantes.remove(cliente_mas_cercano)

    return ruta_optimizada

# =========================================================
# API
# =========================================================
@app.post("/ruta")
def calcular_ruta(data: dict):

    # ===== ORIGIN =====
    origin = data["origin"]

    origin_lat = origin["lat"]
    origin_lng = origin["lng"]

    # ===== CLIENTES =====
    clientes = data["clientes"]

    if len(clientes) == 0:

        return {
            "error": "No hay clientes"
        }

    # =====================================================
    # CLIENTE MÁS LEJANO = DESTINATION
    # =====================================================
    destination_cliente = obtener_cliente_mas_lejano(
        origin_lat,
        origin_lng,
        clientes
    )

    destination = (
        f'{destination_cliente["lat"]},'
        f'{destination_cliente["lng"]}'
    )

    # =====================================================
    # OPTIMIZAR RUTA
    # =====================================================
    ruta_optimizada = optimizar_ruta(
        origin_lat,
        origin_lng,
        clientes,
        destination_cliente
    )

    # =====================================================
    # WAYPOINTS
    # =====================================================
    waypoints = []

    for cliente in ruta_optimizada:

        coord = f'{cliente["lat"]},{cliente["lng"]}'

        waypoints.append(coord)

    # =====================================================
    # RESPONSE
    # =====================================================
    return {

        "origin":
            f"{origin_lat},{origin_lng}",

        "destination":
            destination,

        "waypoints":
            "|".join(waypoints)
    }
