# Guía de capturas para el informe

## Figura 2 — Generación y validación

Ejecutar:

```powershell
py scripts\generar_dataset.py
py scripts\validar_dataset.py
```

La captura debe mostrar:

- 50 usuarios
- 120 productos
- 180 reservas
- 80 reseñas
- 0 errores

## Figura 3 — Cantidad de documentos cargados

Ejecutar:

```powershell
py scripts\cargar_mongodb.py
```

La captura debe mostrar las cuatro cantidades cargadas.

También se puede capturar la vista general de la base `lightrip` en Compass.

## Figura 4 — Documentos de ejemplo

En Compass:

1. Abrir `lightrip`.
2. Abrir cada colección.
3. Mostrar un documento expandido.
4. Procurar que se vean fechas, documentos embebidos, arreglos y números.

Documentos sugeridos:

- `usuarios`: filtro `{ usuario_id: "USR-001" }`
- `productos`: filtro `{ producto_id: "PROD-001" }`
- `reservas`: filtro `{ reserva_id: "RES-001" }`
- `resenas`: filtro `{ resena_id: "REV-001" }`

## Figura 5 — Q1

Filtro de Compass:

```json
{
  "categoria": "Camping",
  "ubicacion.ciudad": "Bariloche",
  "estado": "disponible"
}
```

Resultado esperado: 6 productos.

## Figura 6 — Q2

Filtro:

```json
{
  "categoria": "Camping",
  "subcategoria": "Carpas",
  "especificaciones.capacidad": { "$gte": 4 },
  "especificaciones.impermeabilidad_mm": { "$gte": 3000 },
  "estado": "disponible"
}
```

Resultado esperado: 2 carpas.

## Figuras 7 y 8 — Q3

Ejecutar Q3 desde `consultas/consultas_mongodb.js` o usar la pestaña
Aggregations de Compass.

Resultado esperado:

- 5 productos disponibles.
- `PROD-002` excluido.
- Reserva bloqueante: `RES-002`.
- Estado: `confirmada`.
- Fechas: 12/07/2026 al 14/07/2026.

## Figura 9 — Q4

Filtro:

```json
{
  "usuario_solicitante_id": "USR-001",
  "estado": { "$in": ["pendiente", "confirmada", "activa"] }
}
```

Resultado esperado: 3 reservas.

## Figura 10 — Q5

Ejecutar Q5 desde el archivo de consultas.

Resultado esperado: 3 alquileres finalizados.

## Figura 11 — Q6

Ejecutar Q6 desde el archivo de consultas.

Resultado esperado:

- usuario: `USR-002`
- promedio: 4.6
- cantidad: 5

## Figura 12 — Q7

Ejecutar Q7 desde el archivo de consultas.

Primer resultado esperado:

- producto: `PROD-001`
- nombre: `Carpa térmica de montaña`
- alquileres finalizados: 10
