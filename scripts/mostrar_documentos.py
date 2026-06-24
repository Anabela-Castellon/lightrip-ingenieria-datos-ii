from bson import json_util
from pymongo import MongoClient


def mostrar(titulo: str, documento: dict | None) -> None:
    print(f"\n=== {titulo} ===")

    if documento is None:
        print("No se encontró el documento.")
        return

    print(
        json_util.dumps(
            documento,
            ensure_ascii=False,
            indent=2,
        )
    )


cliente = MongoClient("mongodb://localhost:27017")
db = cliente["lightrip"]

producto = db.productos.find_one(
    {"producto_id": "PROD-001"},
    {
        "_id": 0,
        "producto_id": 1,
        "usuario_propietario_id": 1,
        "nombre": 1,
        "categoria": 1,
        "ubicacion": 1,
        "precio_por_dia": 1,
        "estado": 1,
        "especificaciones": 1,
        "etiquetas": 1,
        "fecha_publicacion": 1,
    },
)

reserva = db.reservas.find_one(
    {"reserva_id": "RES-001"},
    {
        "_id": 0,
        "reserva_id": 1,
        "producto_id": 1,
        "usuario_solicitante_id": 1,
        "usuario_propietario_id": 1,
        "fecha_inicio": 1,
        "fecha_fin": 1,
        "cantidad_dias": 1,
        "precio_total": 1,
        "estado": 1,
        "sincronizada_neo4j": 1,
    },
)

mostrar("DOCUMENTO DE PRODUCTO", producto)
mostrar("DOCUMENTO DE RESERVA", reserva)

cliente.close()