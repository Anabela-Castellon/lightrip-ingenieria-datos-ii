# Guía de capturas — LighTrip

Esta guía permite obtener las evidencias de MongoDB, Neo4j y del flujo integrado entre ambos motores.

Las capturas pueden realizarse desde la terminal de Visual Studio Code, PowerShell, CMD, `mongosh` y Neo4j Browser.

## 1. Preparación previa

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

Verificar que MongoDB se encuentre iniciado:

```powershell
Get-Service MongoDB
```

El estado esperado es:

```text
Running
```

También se debe iniciar la base local desde Neo4j Desktop.

Configurar la contraseña de Neo4j:

```powershell
$env:NEO4J_PASSWORD="TU_CONTRASEÑA"
```

---

## 2. Generación y validación del dataset

Ejecutar:

```powershell
cls
py scripts\generar_dataset.py
py scripts\validar_dataset.py
```

La captura debe mostrar:

```text
Usuarios generados: 50
Productos generados: 120
Reservas generadas: 180
Reseñas generadas: 80
Errores encontrados: 0
```

Nombre sugerido:

```text
evidencias/generacion-validacion.png
```

---

## 3. Carga inicial de MongoDB

Ejecutar:

```powershell
cls
py scripts\cargar_mongodb.py
```

La captura debe mostrar:

```text
Base de datos: lightrip
Usuarios cargados: 50
Productos cargados: 120
Reservas cargadas: 180
Reseñas cargadas: 80
Índices creados correctamente.
```

Nombre sugerido:

```text
evidencias/carga-mongodb.png
```

---

## 4. Documentos almacenados

Ejecutar:

```powershell
cls
py scripts\mostrar_documentos.py
```

La evidencia debe permitir observar:

- Identificadores.
- Documentos embebidos.
- Arreglos.
- Fechas.
- Valores numéricos.
- Referencias entre colecciones.

Nombres sugeridos:

```text
evidencias/documentos-1.png
evidencias/documentos-2.png
```

---

## 5. Consultas Q1 a Q7 — MongoDB

Ejecutar:

```powershell
cls
py scripts\verificar_resultados.py
```

### Q1. Búsqueda por categoría y ubicación

Resultado esperado:

```text
Cantidad: 6
```

Nombre sugerido:

```text
evidencias/q1-camping-bariloche.png
```

### Q2. Filtro por atributos específicos

Resultado esperado:

```text
Cantidad: 2
```

Nombre sugerido:

```text
evidencias/q2-atributos.png
```

### Q3. Disponibilidad por fechas

Resultados esperados:

```text
Productos disponibles: 5
Producto excluido: PROD-002
Reserva bloqueante: RES-002
Estado: confirmada
```

Nombres sugeridos:

```text
evidencias/q3-disponibles.png
evidencias/q3-superposicion.png
```

### Q4. Reservas vigentes

Resultado esperado:

```text
Cantidad: 3
```

Nombre sugerido:

```text
evidencias/q4-reservas-vigentes.png
```

### Q5. Historial de alquileres

Resultado esperado:

```text
Cantidad: 3
```

Nombre sugerido:

```text
evidencias/q5-historial.png
```

### Q6. Reputación

Resultado esperado:

```text
reputacion_promedio: 4.6
cantidad_resenas: 5
```

Nombre sugerido:

```text
evidencias/q6-reputacion.png
```

### Q7. Productos con mayor demanda

Primer resultado esperado:

```text
producto_id: PROD-001
nombre: Carpa térmica de montaña
cantidad_alquileres: 10
```

Nombre sugerido:

```text
evidencias/q7-demanda.png
```

---

## 6. Consultas Q8 a Q10 — Neo4j

Las consultas se ejecutan desde Neo4j Browser.

### Q8. Propietarios con interacciones frecuentes

Resultado esperado para `USR-001`:

| Propietario | Operaciones |
|---|---:|
| `USR-002` | 2 |
| `USR-006` | 1 |

Nombre sugerido:

```text
evidencias/q8-propietarios-frecuentes.png
```

### Q9. Usuarios con propietarios en común

Resultado esperado:

- 9 usuarios similares.
- `USR-009` comparte 2 propietarios con `USR-001`.
- Propietarios compartidos: `USR-002` y `USR-006`.

Nombre sugerido:

```text
evidencias/q9-usuarios-similares.png
```

### Q10. Recomendación social

Neo4j debe devolver 10 propietarios recomendados:

```text
USR-025
USR-005
USR-011
USR-020
USR-027
USR-012
USR-014
USR-013
USR-007
USR-015
```

Nombre sugerido:

```text
evidencias/q10-neo4j-recomendaciones.png
```

En MongoDB, la segunda etapa debe recuperar 24 productos disponibles.

Nombre sugerido:

```text
evidencias/q10-mongodb-productos.png
```

---

## 7. Flujo integrado entre MongoDB y Neo4j

El flujo que debe quedar demostrado es:

```text
Reserva finalizada en MongoDB
        ↓
Sincronización mediante Python
        ↓
Relación ALQUILO_A en Neo4j
        ↓
Consulta analítica sobre el grafo
```

### 7.1 Primera sincronización

Para realizar una ejecución limpia:

1. Cargar nuevamente MongoDB.

```powershell
py scripts\cargar_mongodb.py
```

2. Limpiar el grafo únicamente en el entorno de prueba:

```cypher
MATCH (n)
DETACH DELETE n;
```

3. Ejecutar:

```powershell
cls
py scripts\sincronizar_mongodb_neo4j.py
```

La captura debe mostrar:

```text
Reservas finalizadas pendientes: 90
Reservas nuevas aplicadas: 90
Reservas ya presentes: 0
Errores: 0
Nodos Usuario: 33
Relaciones ALQUILO_A: 88
Sincronización finalizada.
```

Nombre sugerido:

```text
evidencias/integracion-primera-sincronizacion.png
```

### 7.2 Verificación de `RES-001` en Neo4j

Ejecutar:

```cypher
MATCH
  (cliente:Usuario)-[r:ALQUILO_A]->(propietario:Usuario)
WHERE
  "RES-001" IN r.reservas_procesadas
RETURN
  cliente.usuario_id AS cliente,
  propietario.usuario_id AS propietario,
  r.cantidad_operaciones AS operaciones,
  r.ultima_fecha AS ultima_fecha,
  r.categorias AS categorias,
  r.reservas_procesadas AS reservas_procesadas;
```

Resultado esperado:

```text
cliente: USR-001
propietario: USR-002
operaciones: 2
ultima_fecha: 2026-05-15
categorias: ["Camping"]
reservas_procesadas: ["RES-001", "RES-006"]
```

Nombre sugerido:

```text
evidencias/integracion-reserva-neo4j.png
```

### 7.3 Verificación de `RES-001` en MongoDB

Abrir `mongosh` y ejecutar:

```javascript
use lightrip

db.reservas.findOne(
  { reserva_id: "RES-001" },
  {
    _id: 0,
    reserva_id: 1,
    estado: 1,
    sincronizada_neo4j: 1,
    fecha_sincronizacion: 1
  }
);
```

El documento debe mostrar:

```text
reserva_id: RES-001
estado: finalizada
sincronizada_neo4j: true
```

Nombre sugerido:

```text
evidencias/integracion-reserva-mongodb.png
```

### 7.4 Consulta analítica posterior

En Neo4j Browser ejecutar:

```cypher
MATCH
  (:Usuario {usuario_id: "USR-001"})
  -[r:ALQUILO_A]->
  (propietario:Usuario)
RETURN
  propietario.usuario_id AS propietario_id,
  r.cantidad_operaciones AS operaciones,
  r.ultima_fecha AS ultima_fecha
ORDER BY operaciones DESC;
```

Resultado esperado:

| Propietario | Operaciones |
|---|---:|
| `USR-002` | 2 |
| `USR-006` | 1 |

Nombre sugerido:

```text
evidencias/integracion-consulta-analitica.png
```

### 7.5 Control de duplicados

Sin eliminar el grafo, volver a cargar MongoDB:

```powershell
py scripts\cargar_mongodb.py
```

Después ejecutar:

```powershell
cls
py scripts\sincronizar_mongodb_neo4j.py
```

La captura debe mostrar:

```text
Reservas finalizadas pendientes: 90
Reservas nuevas aplicadas: 0
Reservas ya presentes: 90
Errores: 0
Nodos Usuario: 33
Relaciones ALQUILO_A: 88
```

Esto demuestra que las reservas ya procesadas no generan relaciones duplicadas ni aumentan nuevamente los contadores.

Nombre sugerido:

```text
evidencias/integracion-control-duplicados.png
```