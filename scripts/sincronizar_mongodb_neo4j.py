from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from neo4j import GraphDatabase
from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "lightrip"

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


CONSULTA_SINCRONIZACION = """
MERGE (cliente:Usuario {usuario_id: $cliente_id})
MERGE (propietario:Usuario {usuario_id: $propietario_id})
MERGE (cliente)-[r:ALQUILO_A]->(propietario)

ON CREATE SET
    r.cantidad_operaciones = 0,
    r.ultima_fecha = null,
    r.categorias = [],
    r.reservas_procesadas = []

WITH
    r,
    $reserva_id AS reserva_id,
    $categoria AS categoria,
    date($fecha_fin) AS fecha_fin

WITH
    r,
    reserva_id,
    categoria,
    fecha_fin,
    NOT (
        reserva_id IN coalesce(r.reservas_procesadas, [])
    ) AS nueva

FOREACH (_ IN CASE WHEN nueva THEN [1] ELSE [] END |
    SET
        r.cantidad_operaciones =
            coalesce(r.cantidad_operaciones, 0) + 1,

        r.reservas_procesadas =
            coalesce(r.reservas_procesadas, []) + [reserva_id],

        r.categorias =
            CASE
                WHEN categoria IN coalesce(r.categorias, [])
                THEN coalesce(r.categorias, [])
                ELSE coalesce(r.categorias, []) + [categoria]
            END,

        r.ultima_fecha =
            CASE
                WHEN r.ultima_fecha IS NULL
                     OR fecha_fin > r.ultima_fecha
                THEN fecha_fin
                ELSE r.ultima_fecha
            END
)

RETURN nueva AS aplicada
"""


def sincronizar_reserva(
    tx: Any,
    reserva: dict[str, Any],
    categoria: str,
) -> bool:
    fecha_fin = reserva["fecha_fin"]

    if isinstance(fecha_fin, datetime):
        fecha_fin_texto = fecha_fin.date().isoformat()
    else:
        fecha_fin_texto = str(fecha_fin)[:10]

    resultado = tx.run(
        CONSULTA_SINCRONIZACION,
        cliente_id=reserva["usuario_solicitante_id"],
        propietario_id=reserva["usuario_propietario_id"],
        reserva_id=reserva["reserva_id"],
        categoria=categoria,
        fecha_fin=fecha_fin_texto,
    ).single()

    return bool(resultado["aplicada"])


def main() -> None:
    if not NEO4J_PASSWORD:
        print("Falta definir la variable NEO4J_PASSWORD.")
        raise SystemExit(1)

    try:
        mongo = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
        )
        mongo.admin.command("ping")
    except PyMongoError as error:
        print("No fue posible conectarse con MongoDB.")
        print(error)
        raise SystemExit(1) from error

    db = mongo[MONGO_DB]

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )

    try:
        driver.verify_connectivity()
    except Exception as error:
        print("No fue posible conectarse con Neo4j.")
        print(error)
        driver.close()
        mongo.close()
        raise SystemExit(1) from error

    reservas = list(
        db.reservas.find(
            {
                "estado": "finalizada",
                "sincronizada_neo4j": {"$ne": True},
            }
        )
    )

    print("=== SINCRONIZACIÓN MONGODB → NEO4J ===")
    print(f"Reservas finalizadas pendientes: {len(reservas)}")

    aplicadas = 0
    ya_existentes = 0
    errores = 0

    with driver.session(database="neo4j") as session:
        session.run(
            """
            CREATE CONSTRAINT usuario_id_unico IF NOT EXISTS
            FOR (u:Usuario)
            REQUIRE u.usuario_id IS UNIQUE
            """
        ).consume()

        for reserva in reservas:
            producto = db.productos.find_one(
                {"producto_id": reserva["producto_id"]},
                {"_id": 0, "categoria": 1},
            )

            if producto is None:
                errores += 1
                print(
                    f"No se encontró el producto "
                    f"{reserva['producto_id']}."
                )
                continue

            try:
                aplicada = session.execute_write(
                    sincronizar_reserva,
                    reserva,
                    producto["categoria"],
                )

                if aplicada:
                    aplicadas += 1
                else:
                    ya_existentes += 1

                db.reservas.update_one(
                    {"reserva_id": reserva["reserva_id"]},
                    {
                        "$set": {
                            "sincronizada_neo4j": True,
                            "fecha_sincronizacion": datetime.now(
                                timezone.utc
                            ),
                        }
                    },
                )

            except Exception as error:
                errores += 1
                print(
                    f"Error al procesar "
                    f"{reserva['reserva_id']}: {error}"
                )

        cantidades = session.run(
            """
            MATCH (u:Usuario)
            WITH count(u) AS nodos
            OPTIONAL MATCH ()-[r:ALQUILO_A]->()
            RETURN nodos, count(r) AS relaciones
            """
        ).single()

    print(f"Reservas nuevas aplicadas: {aplicadas}")
    print(f"Reservas ya presentes: {ya_existentes}")
    print(f"Errores: {errores}")
    print(f"Nodos Usuario: {cantidades['nodos']}")
    print(
        f"Relaciones ALQUILO_A: "
        f"{cantidades['relaciones']}"
    )
    print("Sincronización finalizada.")

    driver.close()
    mongo.close()


if __name__ == "__main__":
    main()