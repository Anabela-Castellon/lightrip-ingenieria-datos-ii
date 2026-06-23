from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def cargar(nombre: str) -> list[dict[str, Any]]:
    ruta = DATA_DIR / nombre

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Ejecutá primero generar_dataset.py."
        )

    return json.loads(ruta.read_text(encoding="utf-8"))


def fecha_iso(valor: str) -> datetime:
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


def validar() -> list[str]:
    usuarios = cargar("usuarios.json")
    productos = cargar("productos.json")
    reservas = cargar("reservas.json")
    resenas = cargar("resenas.json")

    errores: list[str] = []

    usuarios_id = [usuario["usuario_id"] for usuario in usuarios]
    productos_id = [producto["producto_id"] for producto in productos]
    reservas_id = [reserva["reserva_id"] for reserva in reservas]
    resenas_id = [resena["resena_id"] for resena in resenas]
    emails = [usuario["email"] for usuario in usuarios]

    pruebas = {
        "Identificadores de usuarios únicos": len(usuarios_id) == len(set(usuarios_id)),
        "Identificadores de productos únicos": len(productos_id) == len(set(productos_id)),
        "Identificadores de reservas únicos": len(reservas_id) == len(set(reservas_id)),
        "Identificadores de reseñas únicos": len(resenas_id) == len(set(resenas_id)),
        "Correos únicos": len(emails) == len(set(emails)),
    }

    for nombre, aprobada in pruebas.items():
        if not aprobada:
            errores.append(nombre)

    usuarios_validos = set(usuarios_id)
    productos_validos = set(productos_id)
    reservas_por_id = {
        reserva["reserva_id"]: reserva
        for reserva in reservas
    }

    for producto in productos:
        if producto["usuario_propietario_id"] not in usuarios_validos:
            errores.append(
                f"Producto {producto['producto_id']} con propietario inválido."
            )

    for reserva in reservas:
        reserva_id = reserva["reserva_id"]

        if reserva["producto_id"] not in productos_validos:
            errores.append(
                f"Reserva {reserva_id} con producto inválido."
            )

        if reserva["usuario_solicitante_id"] not in usuarios_validos:
            errores.append(
                f"Reserva {reserva_id} con cliente inválido."
            )

        if reserva["usuario_propietario_id"] not in usuarios_validos:
            errores.append(
                f"Reserva {reserva_id} con propietario inválido."
            )

        if (
            reserva["usuario_solicitante_id"]
            == reserva["usuario_propietario_id"]
        ):
            errores.append(
                f"Reserva {reserva_id}: cliente y propietario coinciden."
            )

        inicio = fecha_iso(reserva["fecha_inicio"])
        fin = fecha_iso(reserva["fecha_fin"])

        if fin <= inicio:
            errores.append(
                f"Reserva {reserva_id}: fechas inválidas."
            )

        dias_calculados = (fin - inicio).days

        if reserva["cantidad_dias"] != dias_calculados:
            errores.append(
                f"Reserva {reserva_id}: duración incorrecta."
            )

        total_calculado = (
            reserva["cantidad_dias"]
            * reserva["precio_por_dia"]
        )

        if reserva["precio_total"] != total_calculado:
            errores.append(
                f"Reserva {reserva_id}: precio total incorrecto."
            )

    for resena in resenas:
        resena_id = resena["resena_id"]
        reserva = reservas_por_id.get(resena["reserva_id"])

        if reserva is None:
            errores.append(
                f"Reseña {resena_id}: reserva inexistente."
            )
            continue

        if reserva["estado"] != "finalizada":
            errores.append(
                f"Reseña {resena_id}: la reserva no está finalizada."
            )

        if not 1 <= resena["puntaje"] <= 5:
            errores.append(
                f"Reseña {resena_id}: puntaje fuera del rango 1 a 5."
            )

        if resena["producto_id"] != reserva["producto_id"]:
            errores.append(
                f"Reseña {resena_id}: producto distinto al de la reserva."
            )

        if (
            resena["usuario_autor_id"]
            != reserva["usuario_solicitante_id"]
        ):
            errores.append(
                f"Reseña {resena_id}: autor distinto al cliente."
            )

        if (
            resena["usuario_destinatario_id"]
            != reserva["usuario_propietario_id"]
        ):
            errores.append(
                f"Reseña {resena_id}: destinatario distinto al propietario."
            )

    print("=== VALIDACIÓN DEL DATASET LIGHTRIP ===")
    print("Identificadores únicos: APROBADA" if not any(
        "Identificadores" in error for error in errores
    ) else "Identificadores únicos: ERROR")
    print("Correos únicos: APROBADA" if "Correos únicos" not in errores
          else "Correos únicos: ERROR")
    print("Referencias válidas: APROBADA" if not any(
        "inválid" in error or "inexistente" in error
        for error in errores
    ) else "Referencias válidas: ERROR")
    print("Cliente distinto del propietario: APROBADA" if not any(
        "cliente y propietario coinciden" in error
        for error in errores
    ) else "Cliente distinto del propietario: ERROR")
    print("Fechas válidas: APROBADA" if not any(
        "fechas inválidas" in error or "duración incorrecta" in error
        for error in errores
    ) else "Fechas válidas: ERROR")
    print("Precios coherentes: APROBADA" if not any(
        "precio total incorrecto" in error
        for error in errores
    ) else "Precios coherentes: ERROR")
    print("Puntajes entre 1 y 5: APROBADA" if not any(
        "puntaje fuera" in error
        for error in errores
    ) else "Puntajes entre 1 y 5: ERROR")
    print("Reseñas asociadas a reservas finalizadas: APROBADA" if not any(
        "no está finalizada" in error
        for error in errores
    ) else "Reseñas asociadas a reservas finalizadas: ERROR")
    print()
    print(f"Errores encontrados: {len(errores)}")

    if errores:
        print("\nDetalle:")
        for error in errores:
            print(f"  - {error}")
    else:
        print("Dataset válido y listo para cargar.")

    return errores


def main() -> None:
    errores = validar()

    if errores:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
