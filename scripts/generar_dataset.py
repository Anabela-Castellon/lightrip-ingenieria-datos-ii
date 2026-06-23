from __future__ import annotations

import json
import random
import unicodedata
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def iso(dt: datetime) -> str:
    """Devuelve una fecha ISO 8601 en UTC."""
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def normalizar(texto: str) -> str:
    """Normaliza texto para usarlo dentro de un correo electrónico."""
    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .replace(" ", ".")
    )


def guardar(nombre: str, datos: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ruta = DATA_DIR / nombre
    ruta.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def generar_dataset() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    random.seed(42)

    nombres = [
        "Martina", "Lucas", "Sofía", "Mateo", "Valentina", "Tomás", "Camila",
        "Nicolás", "Julieta", "Agustín", "Micaela", "Franco", "Carolina",
        "Joaquín", "Lucía", "Federico", "Paula", "Santiago", "Florencia",
        "Bruno", "Ana", "Mariano", "Victoria", "Gonzalo", "Rocío", "Facundo",
        "Milagros", "Leandro", "Candela", "Ignacio", "Belén", "Ramiro",
        "Malena", "Ezequiel", "Delfina", "Juan", "Josefina", "Emiliano",
        "Lara", "Sebastián", "Pilar", "Lautaro", "Catalina", "Benjamín",
        "Aldana", "Matías", "Renata", "Thiago", "Abril", "Alan",
    ]

    apellidos = [
        "López", "García", "Rodríguez", "Fernández", "Gómez", "Martínez",
        "Pérez", "Sánchez", "Romero", "Díaz", "Álvarez", "Torres", "Ruiz",
        "Ramírez", "Flores", "Acosta", "Benítez", "Medina", "Herrera",
        "Suárez", "Molina", "Castro", "Ortiz", "Silva", "Rojas", "Vega",
        "Navarro", "Cabrera", "Morales", "Arias", "Méndez", "Ibarra", "Ponce",
        "Sosa", "Paz", "Vargas", "Correa", "Ramos", "Ferreyra", "Luna",
        "Figueroa", "Mansilla", "Aguirre", "Peralta", "Campos", "Godoy",
        "Quiroga", "Roldán", "Villalba", "Bravo",
    ]

    ubicaciones = [
        {"ciudad": "Buenos Aires", "provincia": "Buenos Aires", "pais": "Argentina"},
        {"ciudad": "Bariloche", "provincia": "Río Negro", "pais": "Argentina"},
        {"ciudad": "Córdoba", "provincia": "Córdoba", "pais": "Argentina"},
        {"ciudad": "Mendoza", "provincia": "Mendoza", "pais": "Argentina"},
        {"ciudad": "Mar del Plata", "provincia": "Buenos Aires", "pais": "Argentina"},
        {"ciudad": "Salta", "provincia": "Salta", "pais": "Argentina"},
        {"ciudad": "Ushuaia", "provincia": "Tierra del Fuego", "pais": "Argentina"},
        {"ciudad": "Rosario", "provincia": "Santa Fe", "pais": "Argentina"},
    ]

    usuarios: list[dict[str, Any]] = []
    for i in range(50):
        usuario_id = f"USR-{i + 1:03d}"
        nombre = nombres[i]
        apellido = apellidos[i]

        usuarios.append(
            {
                "usuario_id": usuario_id,
                "nombre": f"{nombre} {apellido}",
                "email": (
                    f"{normalizar(nombre)}.{normalizar(apellido)}."
                    f"{i + 1}@email.com"
                ),
                "ubicacion": dict(ubicaciones[i % len(ubicaciones)]),
                "fecha_registro": iso(datetime(2026, 1, 1) + timedelta(days=i * 3)),
                "estado": "activo",
            }
        )

    productos_controlados: list[dict[str, Any]] = [
        {
            "producto_id": "PROD-001",
            "usuario_propietario_id": "USR-002",
            "nombre": "Carpa térmica de montaña",
            "descripcion": "Carpa para cuatro personas, apta para montaña.",
            "categoria": "Camping",
            "subcategoria": "Carpas",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 18000,
            "estado": "disponible",
            "especificaciones": {
                "capacidad": 4,
                "impermeabilidad_mm": 3000,
                "cantidad_estaciones": 4,
            },
            "etiquetas": ["camping", "montaña", "impermeable"],
            "fecha_publicacion": "2026-04-15T00:00:00Z",
        },
        {
            "producto_id": "PROD-002",
            "usuario_propietario_id": "USR-003",
            "nombre": "Carpa familiar reforzada",
            "descripcion": "Carpa espaciosa para grupos y familias.",
            "categoria": "Camping",
            "subcategoria": "Carpas",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 22000,
            "estado": "disponible",
            "especificaciones": {
                "capacidad": 6,
                "impermeabilidad_mm": 5000,
                "cantidad_estaciones": 4,
            },
            "etiquetas": ["camping", "familiar", "impermeable"],
            "fecha_publicacion": "2026-04-18T00:00:00Z",
        },
        {
            "producto_id": "PROD-003",
            "usuario_propietario_id": "USR-004",
            "nombre": "Carpa compacta para dos",
            "descripcion": "Carpa liviana para escapadas cortas.",
            "categoria": "Camping",
            "subcategoria": "Carpas",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 12500,
            "estado": "disponible",
            "especificaciones": {
                "capacidad": 2,
                "impermeabilidad_mm": 2000,
                "cantidad_estaciones": 3,
            },
            "etiquetas": ["camping", "liviana"],
            "fecha_publicacion": "2026-04-20T00:00:00Z",
        },
        {
            "producto_id": "PROD-004",
            "usuario_propietario_id": "USR-005",
            "nombre": "Mochila de trekking 60 litros",
            "descripcion": "Mochila con soporte lumbar y cobertor.",
            "categoria": "Camping",
            "subcategoria": "Mochilas",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 9500,
            "estado": "disponible",
            "especificaciones": {
                "capacidad_litros": 60,
                "impermeable": True,
                "peso_kg": 1.8,
            },
            "etiquetas": ["trekking", "mochila", "montaña"],
            "fecha_publicacion": "2026-04-22T00:00:00Z",
        },
        {
            "producto_id": "PROD-005",
            "usuario_propietario_id": "USR-006",
            "nombre": "Bolsa de dormir -10 °C",
            "descripcion": "Bolsa térmica para bajas temperaturas.",
            "categoria": "Camping",
            "subcategoria": "Bolsas de dormir",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 8000,
            "estado": "disponible",
            "especificaciones": {
                "temperatura_minima_c": -10,
                "material": "Sintético",
                "peso_kg": 1.5,
            },
            "etiquetas": ["camping", "frío", "montaña"],
            "fecha_publicacion": "2026-04-24T00:00:00Z",
        },
        {
            "producto_id": "PROD-006",
            "usuario_propietario_id": "USR-007",
            "nombre": "Kit de cocina de camping",
            "descripcion": "Anafe, olla y utensilios para dos personas.",
            "categoria": "Camping",
            "subcategoria": "Cocina",
            "ubicacion": {
                "ciudad": "Bariloche",
                "provincia": "Río Negro",
                "pais": "Argentina",
            },
            "precio_por_dia": 7000,
            "estado": "disponible",
            "especificaciones": {
                "cantidad_personas": 2,
                "incluye_anafe": True,
                "peso_kg": 2.1,
            },
            "etiquetas": ["camping", "cocina", "anafe"],
            "fecha_publicacion": "2026-04-26T00:00:00Z",
        },
    ]

    categorias = {
        "Indumentaria": ["Camperas", "Botas", "Pantalones"],
        "Movilidad": ["Bicicletas", "Monopatines"],
        "Playa": ["Sombrillas", "Reposeras"],
        "Equipaje": ["Valijas", "Bolsos"],
        "Montaña": ["Bastones", "Crampones"],
        "Actividades acuáticas": ["Kayaks", "Tablas SUP"],
        "Camping": ["Carpas", "Mochilas", "Bolsas de dormir", "Cocina"],
    }

    ubicaciones_sin_bariloche = [
        ubicacion for ubicacion in ubicaciones
        if ubicacion["ciudad"] != "Bariloche"
    ]

    def crear_especificaciones(categoria: str, subcategoria: str, i: int) -> dict[str, Any]:
        if subcategoria == "Carpas":
            # Ninguno de estos productos extra cumple simultáneamente Q2.
            return {
                "capacidad": 2 if i % 2 == 0 else 3,
                "impermeabilidad_mm": 2500 if i % 2 == 0 else 1800,
                "cantidad_estaciones": 3,
            }
        if subcategoria == "Camperas":
            return {
                "talle": ["S", "M", "L", "XL"][i % 4],
                "nivel_abrigo": ["medio", "alto"][i % 2],
                "impermeable": bool(i % 2),
            }
        if subcategoria == "Botas":
            return {
                "talle": 36 + i % 10,
                "impermeable": True,
                "tipo_suela": "trekking",
            }
        if subcategoria == "Pantalones":
            return {
                "talle": ["S", "M", "L", "XL"][i % 4],
                "material": "ripstop",
                "impermeable": bool(i % 2),
            }
        if subcategoria == "Bicicletas":
            return {
                "rodado": [26, 27.5, 29][i % 3],
                "tipo_freno": ["disco", "v-brake"][i % 2],
                "cambios": 18 + i % 10,
            }
        if subcategoria == "Monopatines":
            return {
                "autonomia_km": 20 + i % 15,
                "velocidad_max_kmh": 25,
                "electrico": True,
            }
        if subcategoria == "Sombrillas":
            return {"diametro_m": 1.8 + (i % 3) * 0.2, "proteccion_uv": True}
        if subcategoria == "Reposeras":
            return {"posiciones": 3 + i % 3, "material": "aluminio"}
        if subcategoria == "Valijas":
            return {
                "capacidad_litros": 40 + i % 50,
                "tipo": "rígida" if i % 2 else "blanda",
                "ruedas": 4,
            }
        if subcategoria == "Bolsos":
            return {"capacidad_litros": 30 + i % 40, "impermeable": bool(i % 2)}
        if subcategoria == "Bastones":
            return {"material": "aluminio", "regulables": True, "largo_max_cm": 130}
        if subcategoria == "Crampones":
            return {"puntas": 10 + i % 3, "material": "acero", "talle_ajustable": True}
        if subcategoria == "Kayaks":
            return {
                "capacidad_personas": 1 + i % 2,
                "incluye_chaleco": True,
                "largo_m": 3.0 + (i % 5) * 0.1,
            }
        if subcategoria == "Tablas SUP":
            return {"largo_pies": 10 + i % 3, "inflable": True, "incluye_remo": True}
        if subcategoria == "Mochilas":
            return {"capacidad_litros": 40 + i % 30, "impermeable": bool(i % 2), "peso_kg": 1.2}
        if subcategoria == "Bolsas de dormir":
            return {"temperatura_minima_c": -5 - i % 10, "material": "Sintético", "peso_kg": 1.4}
        if subcategoria == "Cocina":
            return {"cantidad_personas": 2 + i % 4, "incluye_anafe": bool(i % 2), "peso_kg": 2.0}
        return {"detalle": "estándar"}

    productos = productos_controlados.copy()
    ciclo_categorias = list(categorias.keys())

    for i in range(7, 121):
        categoria = ciclo_categorias[(i - 7) % len(ciclo_categorias)]
        subcategoria = categorias[categoria][(i - 7) % len(categorias[categoria])]

        if categoria == "Camping":
            ubicacion = ubicaciones_sin_bariloche[
                (i - 7) % len(ubicaciones_sin_bariloche)
            ]
        else:
            ubicacion = ubicaciones[(i - 7) % len(ubicaciones)]

        propietario_numero = 2 + ((i * 11) % 49)

        # Propietarios controlados para las recomendaciones sociales futuras.
        if i == 7:
            propietario_numero = 14
        elif i == 8:
            propietario_numero = 27
        elif i == 9:
            propietario_numero = 35

        productos.append(
            {
                "producto_id": f"PROD-{i:03d}",
                "usuario_propietario_id": f"USR-{propietario_numero:03d}",
                "nombre": f"{subcategoria} modelo {i:03d}",
                "descripcion": (
                    f"Producto de {categoria.lower()} preparado "
                    "para alquiler temporal."
                ),
                "categoria": categoria,
                "subcategoria": subcategoria,
                "ubicacion": dict(ubicacion),
                "precio_por_dia": 5000 + (i % 20) * 1250,
                "estado": "disponible" if i % 10 != 0 else "pausado",
                "especificaciones": crear_especificaciones(categoria, subcategoria, i),
                "etiquetas": [categoria.lower(), subcategoria.lower(), "viaje"],
                "fecha_publicacion": iso(datetime(2026, 2, 1) + timedelta(days=i)),
            }
        )

    productos_por_id = {
        producto["producto_id"]: producto
        for producto in productos
    }

    reservas: list[dict[str, Any]] = []

    def agregar_reserva(
        producto_id: str,
        cliente_id: str,
        inicio: datetime,
        fin: datetime,
        estado: str,
    ) -> None:
        producto = productos_por_id[producto_id]
        propietario_id = producto["usuario_propietario_id"]

        if cliente_id == propietario_id:
            raise ValueError("El cliente no puede ser el propietario.")

        reserva_id = f"RES-{len(reservas) + 1:03d}"
        cantidad_dias = (fin - inicio).days
        precio_diario = producto["precio_por_dia"]

        reservas.append(
            {
                "reserva_id": reserva_id,
                "producto_id": producto_id,
                "usuario_solicitante_id": cliente_id,
                "usuario_propietario_id": propietario_id,
                "fecha_inicio": iso(inicio),
                "fecha_fin": iso(fin),
                "cantidad_dias": cantidad_dias,
                "precio_por_dia": precio_diario,
                "precio_total": cantidad_dias * precio_diario,
                "estado": estado,
                "sincronizada_neo4j": False,
                "fecha_sincronizacion": None,
                "fecha_creacion": iso(inicio - timedelta(days=15)),
            }
        )

    # Casos controlados de USR-001.
    agregar_reserva(
        "PROD-001", "USR-001",
        datetime(2026, 5, 10), datetime(2026, 5, 15),
        "finalizada",
    )
    agregar_reserva(
        "PROD-002", "USR-001",
        datetime(2026, 7, 12), datetime(2026, 7, 14),
        "confirmada",
    )
    agregar_reserva(
        "PROD-003", "USR-001",
        datetime(2026, 8, 1), datetime(2026, 8, 5),
        "pendiente",
    )
    agregar_reserva(
        "PROD-004", "USR-001",
        datetime(2026, 6, 20), datetime(2026, 6, 25),
        "activa",
    )
    agregar_reserva(
        "PROD-005", "USR-001",
        datetime(2026, 4, 1), datetime(2026, 4, 4),
        "finalizada",
    )
    agregar_reserva(
        "PROD-001", "USR-001",
        datetime(2026, 1, 10), datetime(2026, 1, 13),
        "finalizada",
    )

    # Casos superpuestos que no bloquean por su estado.
    agregar_reserva(
        "PROD-005", "USR-010",
        datetime(2026, 7, 11), datetime(2026, 7, 13),
        "cancelada",
    )
    agregar_reserva(
        "PROD-006", "USR-011",
        datetime(2026, 7, 10), datetime(2026, 7, 15),
        "rechazada",
    )
    agregar_reserva(
        "PROD-004", "USR-012",
        datetime(2026, 7, 10), datetime(2026, 7, 15),
        "finalizada",
    )

    # PROD-001 queda como el producto con mayor demanda: 10 finalizadas.
    alquileres_prod_001 = [
        ("USR-008", datetime(2026, 2, 1)),
        ("USR-009", datetime(2026, 2, 8)),
        ("USR-011", datetime(2026, 2, 15)),
        ("USR-012", datetime(2026, 2, 22)),
        ("USR-013", datetime(2026, 3, 1)),
        ("USR-014", datetime(2026, 3, 8)),
        ("USR-015", datetime(2026, 3, 15)),
        ("USR-016", datetime(2026, 3, 22)),
    ]

    for cliente_id, inicio in alquileres_prod_001:
        agregar_reserva(
            "PROD-001",
            cliente_id,
            inicio,
            inicio + timedelta(days=3),
            "finalizada",
        )

    # Caminos sociales controlados para Neo4j.
    agregar_reserva(
        "PROD-007", "USR-008",
        datetime(2026, 4, 5), datetime(2026, 4, 8),
        "finalizada",
    )
    agregar_reserva(
        "PROD-005", "USR-009",
        datetime(2026, 4, 15), datetime(2026, 4, 18),
        "finalizada",
    )
    agregar_reserva(
        "PROD-008", "USR-009",
        datetime(2026, 4, 20), datetime(2026, 4, 23),
        "finalizada",
    )
    agregar_reserva(
        "PROD-005", "USR-010",
        datetime(2026, 5, 1), datetime(2026, 5, 3),
        "finalizada",
    )
    agregar_reserva(
        "PROD-005", "USR-010",
        datetime(2026, 5, 7), datetime(2026, 5, 9),
        "finalizada",
    )
    agregar_reserva(
        "PROD-009", "USR-010",
        datetime(2026, 5, 12), datetime(2026, 5, 15),
        "finalizada",
    )

    cantidades_objetivo = {
        "finalizada": 90,
        "confirmada": 18,
        "pendiente": 18,
        "activa": 18,
        "cancelada": 18,
        "rechazada": 18,
    }

    propietarios_sociales = {
        "USR-002", "USR-006", "USR-014", "USR-027", "USR-035"
    }

    candidatos = [
        producto["producto_id"]
        for producto in productos[9:]
        if producto["usuario_propietario_id"] not in propietarios_sociales
    ]

    cantidades_actuales = Counter(
        reserva["estado"] for reserva in reservas
    )

    secuencia = 0

    for estado, cantidad_objetivo in cantidades_objetivo.items():
        faltantes = cantidad_objetivo - cantidades_actuales[estado]

        for j in range(faltantes):
            producto_id = candidatos[
                (secuencia * 7 + j) % len(candidatos)
            ]
            propietario_id = productos_por_id[
                producto_id
            ]["usuario_propietario_id"]

            numero_cliente = 11 + ((secuencia * 13 + j * 5) % 40)
            cliente_id = f"USR-{numero_cliente:03d}"

            if cliente_id == propietario_id:
                numero_cliente = 11 + ((numero_cliente - 10) % 40)
                cliente_id = f"USR-{numero_cliente:03d}"

                if cliente_id == propietario_id:
                    cliente_id = (
                        "USR-050"
                        if propietario_id != "USR-050"
                        else "USR-049"
                    )

            if estado == "finalizada":
                inicio = datetime(2026, 1, 10) + timedelta(
                    days=(secuencia * 5 + j * 2) % 140
                )
            elif estado == "activa":
                inicio = datetime(2026, 6, 18) + timedelta(
                    days=(secuencia + j) % 5
                )
            else:
                inicio = datetime(2026, 7, 1) + timedelta(
                    days=(secuencia * 3 + j * 4) % 120
                )

            duracion = 2 + ((secuencia + j) % 6)

            agregar_reserva(
                producto_id,
                cliente_id,
                inicio,
                inicio + timedelta(days=duracion),
                estado,
            )

            secuencia += 1

    reservas_finalizadas = [
        reserva
        for reserva in reservas
        if reserva["estado"] == "finalizada"
    ]

    finalizadas_usr_002 = [
        reserva
        for reserva in reservas_finalizadas
        if reserva["usuario_propietario_id"] == "USR-002"
    ]

    finalizadas_otro_propietario = [
        reserva
        for reserva in reservas_finalizadas
        if reserva["usuario_propietario_id"] != "USR-002"
    ]

    if (
        len(finalizadas_usr_002) < 5
        or len(finalizadas_otro_propietario) < 75
    ):
        raise RuntimeError(
            "No existen suficientes reservas para generar las reseñas."
        )

    reservas_para_resenar = (
        finalizadas_usr_002[:5]
        + finalizadas_otro_propietario[:75]
    )

    comentarios = [
        "Excelente experiencia y producto en muy buen estado.",
        "El alquiler fue correcto y la comunicación fue clara.",
        "Producto cuidado y entrega puntual.",
        "Buena atención durante toda la operación.",
        "Cumplió con lo publicado y volvería a alquilar.",
    ]

    puntajes_usr_002 = [5, 4, 5, 4, 5]

    resenas: list[dict[str, Any]] = []

    for i, reserva in enumerate(reservas_para_resenar):
        fecha_fin = datetime.fromisoformat(
            reserva["fecha_fin"].replace("Z", "+00:00")
        ).replace(tzinfo=None)

        resenas.append(
            {
                "resena_id": f"REV-{i + 1:03d}",
                "reserva_id": reserva["reserva_id"],
                "producto_id": reserva["producto_id"],
                "usuario_autor_id": reserva["usuario_solicitante_id"],
                "usuario_destinatario_id": reserva["usuario_propietario_id"],
                "puntaje": (
                    puntajes_usr_002[i]
                    if i < 5
                    else 3 + (i % 3)
                ),
                "comentario": comentarios[i % len(comentarios)],
                "fecha": iso(fecha_fin + timedelta(days=1)),
            }
        )

    return usuarios, productos, reservas, resenas


def main() -> None:
    usuarios, productos, reservas, resenas = generar_dataset()

    guardar("usuarios.json", usuarios)
    guardar("productos.json", productos)
    guardar("reservas.json", reservas)
    guardar("resenas.json", resenas)

    print("=== GENERACIÓN DEL DATASET LIGHTRIP ===")
    print(f"Usuarios generados: {len(usuarios)}")
    print(f"Productos generados: {len(productos)}")
    print(f"Reservas generadas: {len(reservas)}")
    print(f"Reseñas generadas: {len(resenas)}")
    print()
    print("Distribución de estados de reservas:")
    for estado, cantidad in sorted(
        Counter(reserva["estado"] for reserva in reservas).items()
    ):
        print(f"  - {estado}: {cantidad}")
    print()
    print(f"Archivos creados en: {DATA_DIR}")


if __name__ == "__main__":
    main()
