# Guía de capturas — MongoDB desde terminal

Esta guía permite obtener las Figuras 2 a 12 del informe sin utilizar MongoDB Compass.

Las evidencias se generan desde la terminal de Visual Studio Code, PowerShell o CMD.

## Preparación previa

Abrir una terminal en la raíz del repositorio.

### PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### CMD

```cmd
.venv\Scripts\activate.bat
```

Verificar que aparezca:

```text
(.venv)
```

También se debe comprobar que MongoDB se encuentre en ejecución:

```powershell
Get-Service MongoDB
```

El estado esperado es:

```text
Running
```

---

## Figura 2 — Generación y validación del dataset sintético

Ejecutar:

```powershell
cls
py scripts\generar_dataset.py
py scripts\validar_dataset.py
```

La captura debe mostrar:

- Usuarios generados: 50.
- Productos generados: 120.
- Reservas generadas: 180.
- Reseñas generadas: 80.
- Todas las validaciones en `APROBADA`.
- Errores encontrados: 0.

Texto para el informe:

```text
El proceso generó 50 usuarios, 120 productos, 180 reservas y 80 reseñas. Las validaciones finalizaron con 0 errores.
```

Nombre sugerido:

```text
evidencias/figura-02-generacion-validacion.png
```

---

## Figura 3 — Cantidad de documentos cargados en MongoDB

Ejecutar:

```powershell
cls
py scripts\cargar_mongodb.py
```

La captura debe mostrar:

- Base de datos: `lightrip`.
- Usuarios cargados: 50.
- Productos cargados: 120.
- Reservas cargadas: 180.
- Reseñas cargadas: 80.
- Índices creados correctamente.

Tabla para el informe:

| Colección | Generados | Cargados |
|---|---:|---:|
| usuarios | 50 | 50 |
| productos | 120 | 120 |
| reservas | 180 | 180 |
| resenas | 80 | 80 |

Texto para el informe:

```text
Las cantidades generadas y cargadas coinciden.
```

Nombre sugerido:

```text
evidencias/figura-03-carga-mongodb.png
```

---

## Figura 4 — Ejemplos de documentos almacenados en MongoDB

Ejecutar:

```powershell
cls
py scripts\mostrar_documentos.py
```

El script muestra:

- Un usuario.
- Un producto.
- Una reserva.
- Una reseña.

Como la salida puede ser extensa, se pueden tomar dos capturas:

1. Usuario y producto.
2. Reserva y reseña.

La evidencia debe permitir observar:

- Identificadores.
- Documentos embebidos.
- Arreglos.
- Fechas.
- Valores numéricos.
- Referencias entre colecciones.

Texto para el informe:

```text
La evidencia permite comprobar el almacenamiento de identificadores, fechas, documentos embebidos, arreglos y valores numéricos. En el producto se observan la ubicación y las especificaciones como documentos embebidos, mientras que las etiquetas se almacenan como un arreglo. En la reserva y la reseña se visualizan las referencias entre las entidades.
```

Nombres sugeridos:

```text
evidencias/figura-04-documentos-1.png
evidencias/figura-04-documentos-2.png
```

---

## Figuras 5 a 12 — Consultas Q1 a Q7

Ejecutar:

```powershell
cls
py scripts\verificar_resultados.py
```

El script imprime todas las consultas en orden.

Para obtener capturas más legibles, se recomienda agrandar la terminal y tomar una captura por bloque.

---

## Figura 5 — Q1. Productos de Camping en Bariloche

Buscar en la salida:

```text
=== Q1 - Camping disponible en Bariloche ===
```

Resultado esperado:

```text
Cantidad: 6
```

Texto para el informe:

```text
La consulta devolvió 6 productos que cumplen la categoría, ciudad y estado solicitados.
```

Nombre sugerido:

```text
evidencias/figura-05-q1.png
```

---

## Figura 6 — Q2. Carpas filtradas por atributos específicos

Buscar:

```text
=== Q2 - Carpas por atributos específicos ===
```

Resultado esperado:

```text
Cantidad: 2
```

Texto para el informe:

```text
Se recuperaron 2 carpas con capacidad mínima de cuatro personas e impermeabilidad igual o superior a 3000 mm.
```

Nombre sugerido:

```text
evidencias/figura-06-q2.png
```

---

## Figura 7 — Q3. Productos disponibles entre fechas

Buscar:

```text
=== Q3 - Disponibilidad del 10 al 15 de julio de 2026 ===
```

Resultado esperado:

```text
Cantidad: 5
```

Texto para el informe:

```text
La consulta devolvió 5 productos sin reservas bloqueantes superpuestas.
```

Nombre sugerido:

```text
evidencias/figura-07-q3-disponibles.png
```

---

## Figura 8 — Q3. Producto excluido por superposición

Buscar:

```text
=== Q3 - Producto excluido por superposición ===
```

Resultado esperado:

```text
producto_id: PROD-002
reserva_id: RES-002
estado: confirmada
```

Texto para el informe:

```text
El producto PROD-002 fue excluido porque posee una reserva con estado confirmada que se superpone con el período solicitado.
```

Nombre sugerido:

```text
evidencias/figura-08-q3-excluido.png
```

---

## Figura 9 — Q4. Reservas vigentes de USR-001

Buscar:

```text
=== Q4 - Reservas activas de USR-001 ===
```

Resultado esperado:

```text
Cantidad: 3
```

Texto para el informe:

```text
El usuario posee 3 reservas pendientes, confirmadas o activas.
```

Nombre sugerido:

```text
evidencias/figura-09-q4.png
```

---

## Figura 10 — Q5. Historial de alquileres de USR-001

Buscar:

```text
=== Q5 - Historial de alquileres de USR-001 ===
```

Resultado esperado:

```text
Cantidad: 3
```

Texto para el informe:

```text
Se recuperaron 3 reservas finalizadas junto con la información principal de los productos alquilados.
```

Nombre sugerido:

```text
evidencias/figura-10-q5.png
```

---

## Figura 11 — Q6. Reputación de USR-002

Buscar:

```text
=== Q6 - Reputación de USR-002 ===
```

Resultado esperado:

```text
reputacion_promedio: 4.6
cantidad_resenas: 5
```

Texto para el informe:

```text
El usuario obtuvo una reputación promedio de 4,6, calculada a partir de 5 reseñas.
```

Nombre sugerido:

```text
evidencias/figura-11-q6.png
```

---

## Figura 12 — Q7. Productos con mayor demanda

Buscar:

```text
=== Q7 - Productos con mayor demanda ===
```

El primer resultado esperado es:

```text
producto_id: PROD-001
nombre: Carpa térmica de montaña
cantidad_alquileres: 10
```

Texto para el informe:

```text
El producto con mayor actividad fue Carpa térmica de montaña, con 10 alquileres finalizados.
```

Nombre sugerido:

```text
evidencias/figura-12-q7.png
```

---

## Guardar las evidencias en GitHub

Después de guardar las capturas dentro de `evidencias/`:

```powershell
git status
git add evidencias scripts/mostrar_documentos.py README.md GUIA_CAPTURAS.md
git commit -m "Actualizar guía y evidencias de MongoDB por terminal"
git push
```

Las capturas quedarán asociadas con los mismos números utilizados en el informe.
