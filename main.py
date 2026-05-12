from fastapi import FastAPI
from math import sqrt

app = FastAPI()

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }

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

    # ===== CLIENTE MÁS LEJANO =====
    cliente_mas_lejano = None
    distancia_maxima = -1

    for cliente in clientes:

        lat = cliente["lat"]
        lng = cliente["lng"]

        distancia = sqrt(
            (lat - origin_lat) ** 2 +
            (lng - origin_lng) ** 2
        )

        if distancia > distancia_maxima:

            distancia_maxima = distancia
            cliente_mas_lejano = cliente

    # ===== DESTINATION =====
    destination = (
        f'{cliente_mas_lejano["lat"]},'
        f'{cliente_mas_lejano["lng"]}'
    )

    # ===== WAYPOINTS =====
    waypoints = []

    for cliente in clientes:

        coord = f'{cliente["lat"]},{cliente["lng"]}'

        if coord != destination:
            waypoints.append(coord)

    # ===== RESPONSE =====
    return {

        "origin":
            f"{origin_lat},{origin_lng}",

        "destination":
            destination,

        "waypoints":
            "|".join(waypoints)
    }
