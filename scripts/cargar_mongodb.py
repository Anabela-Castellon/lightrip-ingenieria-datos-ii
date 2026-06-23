from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "lightrip")


def cargar_json(nombre: str) -> list[dict[str, Any]]:
    ruta = DATA_DIR / nombre

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Ejecutá primero generar_dataset.py."
        )

    return json.loads(ruta.read_text(encoding="utf-8"))


def convertir_fecha(valor: str | None) -> datetime | None:
    if valor is None:
        return None

    return datetime.fromisoformat(
        valor.replace("Z", "+00:00")
    )


def convertir_fechas(
    documentos: list[dict[str, Any]],
    campos: list[str],
) -> list[dict[str, Any]]:
    resultado: list[dict[str, Any]] = []

    for documento in documentos:
        copia = dict(documento)

        for campo in campos:
            if campo in copia:
                copia[campo] = convertir_fecha(copia[campo])

        resultado.append(copia)

    return resultado


def crear_indices(db: Any) -> None:
    db.usuarios.create_index(
        [("usuario_id", ASCENDING)],
        unique=True,
        name="ux_usuarios_usuario_id",
    )
    db.usuarios.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="ux_usuarios_email",
    )

    db.productos.create_index(
        [("producto_id", ASCENDING)],
        unique=True,
        name="ux_productos_producto_id",
    )
    db.productos.create_index(
        [
            ("categoria", ASCENDING),
            ("ubicacion.ciudad", ASCENDING),
            ("estado", ASCENDING),
        ],
        name="ix_productos_categoria_ciudad_estado",
    )
    db.productos.create_index(
        [("precio_por_dia", ASCENDING)],
        name="ix_productos_precio",
    )

    db.reservas.create_index(
        [("reserva_id", ASCENDING)],
        unique=True,
        name="ux_reservas_reserva_id",
    )
    db.reservas.create_index(
        [
            ("producto_id", ASCENDING),
            ("estado", ASCENDING),
            ("fecha_inicio", ASCENDING),
            ("fecha_fin", ASCENDING),
        ],
        name="ix_reservas_disponibilidad",
    )
    db.reservas.create_index(
        [
            ("usuario_solicitante_id", ASCENDING),
            ("estado", ASCENDING),
            ("fecha_inicio", ASCENDING),
        ],
        name="ix_reservas_usuario_estado_fecha",
    )
    db.reservas.create_index(
        [
            ("estado", ASCENDING),
            ("sincronizada_neo4j", ASCENDING),
        ],
        name="ix_reservas_sincronizacion",
    )

    db.resenas.create_index(
        [("resena_id", ASCENDING)],
        unique=True,
        name="ux_resenas_resena_id",
    )
    db.resenas.create_index(
        [
            ("usuario_destinatario_id", ASCENDING),
            ("fecha", DESCENDING),
        ],
        name="ix_resenas_destinatario_fecha",
    )


def main() -> None:
    usuarios = convertir_fechas(
        cargar_json("usuarios.json"),
        ["fecha_registro"],
    )
    productos = convertir_fechas(
        cargar_json("productos.json"),
        ["fecha_publicacion"],
    )
    reservas = convertir_fechas(
        cargar_json("reservas.json"),
        [
            "fecha_inicio",
            "fecha_fin",
            "fecha_sincronizacion",
            "fecha_creacion",
        ],
    )
    resenas = convertir_fechas(
        cargar_json("resenas.json"),
        ["fecha"],
    )

    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
        )
        cliente.admin.command("ping")
    except PyMongoError as error:
        print("No fue posible conectarse con MongoDB.")
        print(f"URI utilizada: {MONGO_URI}")
        print(f"Detalle: {error}")
        raise SystemExit(1) from error

    # Se elimina la base anterior para que la ejecución sea reproducible.
    cliente.drop_database(DB_NAME)
    db = cliente[DB_NAME]

    db.usuarios.insert_many(usuarios)
    db.productos.insert_many(productos)
    db.reservas.insert_many(reservas)
    db.resenas.insert_many(resenas)

    crear_indices(db)

    print("=== CARGA EN MONGODB ===")
    print(f"Base de datos: {DB_NAME}")
    print(f"Usuarios cargados: {db.usuarios.count_documents({})}")
    print(f"Productos cargados: {db.productos.count_documents({})}")
    print(f"Reservas cargadas: {db.reservas.count_documents({})}")
    print(f"Reseñas cargadas: {db.resenas.count_documents({})}")
    print()
    print("Índices creados correctamente.")
    print("Conexión finalizada.")

    cliente.close()


if __name__ == "__main__":
    main()
