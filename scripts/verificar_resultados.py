from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bson import json_util
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parents[1]
EVIDENCIAS_DIR = BASE_DIR / "evidencias"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "lightrip")


def mostrar_documentos(
    titulo: str,
    documentos: list[dict[str, Any]],
) -> None:
    print(f"\n=== {titulo} ===")
    print(f"Cantidad: {len(documentos)}")
    print(json_util.dumps(
        documentos,
        ensure_ascii=False,
        indent=2,
    ))


def main() -> None:
    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
        )
        cliente.admin.command("ping")
    except PyMongoError as error:
        print("No fue posible conectarse con MongoDB.")
        print(f"Detalle: {error}")
        raise SystemExit(1) from error

    db = cliente[DB_NAME]
    resultados: dict[str, Any] = {}

    q1 = list(
        db.productos.find(
            {
                "categoria": "Camping",
                "ubicacion.ciudad": "Bariloche",
                "estado": "disponible",
            },
            {
                "_id": 0,
                "producto_id": 1,
                "nombre": 1,
                "categoria": 1,
                "ubicacion": 1,
                "precio_por_dia": 1,
            },
        ).sort("producto_id", 1)
    )
    resultados["Q1"] = q1
    mostrar_documentos(
        "Q1 - Camping disponible en Bariloche",
        q1,
    )

    q2 = list(
        db.productos.find(
            {
                "categoria": "Camping",
                "subcategoria": "Carpas",
                "especificaciones.capacidad": {"$gte": 4},
                "especificaciones.impermeabilidad_mm": {"$gte": 3000},
                "estado": "disponible",
            },
            {
                "_id": 0,
                "producto_id": 1,
                "nombre": 1,
                "especificaciones": 1,
                "precio_por_dia": 1,
            },
        ).sort("producto_id", 1)
    )
    resultados["Q2"] = q2
    mostrar_documentos(
        "Q2 - Carpas por atributos específicos",
        q2,
    )

    inicio = datetime(2026, 7, 10, tzinfo=timezone.utc)
    fin = datetime(2026, 7, 15, tzinfo=timezone.utc)

    q3_pipeline = [
        {
            "$match": {
                "categoria": "Camping",
                "ubicacion.ciudad": "Bariloche",
                "estado": "disponible",
            }
        },
        {
            "$lookup": {
                "from": "reservas",
                "let": {"productoId": "$producto_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {
                                        "$eq": [
                                            "$producto_id",
                                            "$$productoId",
                                        ]
                                    },
                                    {
                                        "$in": [
                                            "$estado",
                                            [
                                                "pendiente",
                                                "confirmada",
                                                "activa",
                                            ],
                                        ]
                                    },
                                    {"$lt": ["$fecha_inicio", fin]},
                                    {"$gt": ["$fecha_fin", inicio]},
                                ]
                            }
                        }
                    }
                ],
                "as": "reservas_bloqueantes",
            }
        },
        {
            "$match": {
                "reservas_bloqueantes": {"$size": 0}
            }
        },
        {
            "$project": {
                "_id": 0,
                "producto_id": 1,
                "nombre": 1,
                "categoria": 1,
                "ubicacion": 1,
                "precio_por_dia": 1,
            }
        },
        {"$sort": {"producto_id": 1}},
    ]

    q3 = list(db.productos.aggregate(q3_pipeline))
    resultados["Q3_disponibles"] = q3
    mostrar_documentos(
        "Q3 - Disponibilidad del 10 al 15 de julio de 2026",
        q3,
    )

    candidatos_q3 = {
        documento["producto_id"]
        for documento in q1
    }
    disponibles_q3 = {
        documento["producto_id"]
        for documento in q3
    }
    excluidos_q3 = sorted(
        candidatos_q3 - disponibles_q3
    )

    reservas_excluidas = list(
        db.reservas.find(
            {
                "producto_id": {"$in": excluidos_q3},
                "estado": {
                    "$in": ["pendiente", "confirmada", "activa"]
                },
                "fecha_inicio": {"$lt": fin},
                "fecha_fin": {"$gt": inicio},
            },
            {
                "_id": 0,
                "reserva_id": 1,
                "producto_id": 1,
                "estado": 1,
                "fecha_inicio": 1,
                "fecha_fin": 1,
            },
        )
    )
    resultados["Q3_excluidos"] = reservas_excluidas
    mostrar_documentos(
        "Q3 - Producto excluido por superposición",
        reservas_excluidas,
    )

    q4 = list(
        db.reservas.find(
            {
                "usuario_solicitante_id": "USR-001",
                "estado": {
                    "$in": ["pendiente", "confirmada", "activa"]
                },
            },
            {
                "_id": 0,
                "reserva_id": 1,
                "producto_id": 1,
                "fecha_inicio": 1,
                "fecha_fin": 1,
                "precio_total": 1,
                "estado": 1,
            },
        ).sort("fecha_inicio", 1)
    )
    resultados["Q4"] = q4
    mostrar_documentos(
        "Q4 - Reservas activas de USR-001",
        q4,
    )

    q5_pipeline = [
        {
            "$match": {
                "usuario_solicitante_id": "USR-001",
                "estado": "finalizada",
            }
        },
        {
            "$lookup": {
                "from": "productos",
                "localField": "producto_id",
                "foreignField": "producto_id",
                "as": "producto",
            }
        },
        {"$unwind": "$producto"},
        {
            "$project": {
                "_id": 0,
                "reserva_id": 1,
                "fecha_inicio": 1,
                "fecha_fin": 1,
                "precio_total": 1,
                "producto_id": "$producto.producto_id",
                "producto": "$producto.nombre",
                "categoria": "$producto.categoria",
            }
        },
        {"$sort": {"fecha_fin": -1}},
    ]

    q5 = list(db.reservas.aggregate(q5_pipeline))
    resultados["Q5"] = q5
    mostrar_documentos(
        "Q5 - Historial de alquileres de USR-001",
        q5,
    )

    q6_pipeline = [
        {
            "$match": {
                "usuario_destinatario_id": "USR-002"
            }
        },
        {
            "$group": {
                "_id": "$usuario_destinatario_id",
                "reputacion_promedio": {"$avg": "$puntaje"},
                "cantidad_resenas": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "usuario_id": "$_id",
                "reputacion_promedio": {
                    "$round": ["$reputacion_promedio", 2]
                },
                "cantidad_resenas": 1,
            }
        },
    ]

    q6 = list(db.resenas.aggregate(q6_pipeline))
    resultados["Q6"] = q6
    mostrar_documentos(
        "Q6 - Reputación de USR-002",
        q6,
    )

    q7_pipeline = [
        {"$match": {"estado": "finalizada"}},
        {
            "$group": {
                "_id": "$producto_id",
                "cantidad_alquileres": {"$sum": 1},
                "ingresos_generados": {"$sum": "$precio_total"},
            }
        },
        {
            "$sort": {
                "cantidad_alquileres": -1,
                "ingresos_generados": -1,
            }
        },
        {"$limit": 10},
        {
            "$lookup": {
                "from": "productos",
                "localField": "_id",
                "foreignField": "producto_id",
                "as": "producto",
            }
        },
        {"$unwind": "$producto"},
        {
            "$project": {
                "_id": 0,
                "producto_id": "$_id",
                "nombre": "$producto.nombre",
                "categoria": "$producto.categoria",
                "cantidad_alquileres": 1,
                "ingresos_generados": 1,
            }
        },
    ]

    q7 = list(db.reservas.aggregate(q7_pipeline))
    resultados["Q7"] = q7
    mostrar_documentos(
        "Q7 - Productos con mayor demanda",
        q7,
    )

    EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
    salida = EVIDENCIAS_DIR / "resultados_mongodb.json"
    salida.write_text(
        json_util.dumps(
            resultados,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n=== RESUMEN PARA COMPLETAR EL INFORME ===")
    print(f"Q1: {len(q1)} productos.")
    print(f"Q2: {len(q2)} carpas.")
    print(
        f"Q3: {len(q3)} disponibles y "
        f"{len(excluidos_q3)} excluido(s): "
        f"{', '.join(excluidos_q3)}."
    )
    print(f"Q4: {len(q4)} reservas vigentes.")
    print(f"Q5: {len(q5)} alquileres finalizados.")
    if q6:
        print(
            "Q6: promedio "
            f"{q6[0]['reputacion_promedio']} sobre "
            f"{q6[0]['cantidad_resenas']} reseñas."
        )
    if q7:
        print(
            "Q7: "
            f"{q7[0]['nombre']} ({q7[0]['producto_id']}) "
            f"con {q7[0]['cantidad_alquileres']} alquileres."
        )
    print(f"\nResultados guardados en: {salida}")

    cliente.close()


if __name__ == "__main__":
    main()
