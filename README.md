# LighTrip — Ingeniería de Datos II

Repositorio del Trabajo Práctico Integrador de Ingeniería de Datos II.

LighTrip es una propuesta de plataforma de alquiler temporal de objetos de viaje entre usuarios. El trabajo se concentra en la implementación y validación de la capa de datos mediante una arquitectura NoSQL con persistencia políglota.

## Tecnologías utilizadas

- **MongoDB:** almacenamiento operativo de usuarios, productos, reservas y reseñas.
- **Neo4j:** representación y análisis de relaciones entre clientes y propietarios.
- **Python:** generación, validación, carga, consultas y sincronización entre motores.

MongoDB funciona como fuente principal de los datos. Neo4j mantiene una representación derivada de los alquileres finalizados mediante relaciones `ALQUILO_A`.

## Estructura del proyecto

```text
lightrip-ingenieria-datos-ii/
│
├── consultas/
│   └── consultas_mongodb.js
│
├── data/
│   ├── usuarios.json
│   ├── productos.json
│   ├── reservas.json
│   └── resenas.json
│
├── evidencias/
│
├── scripts/
│   ├── generar_dataset.py
│   ├── validar_dataset.py
│   ├── cargar_mongodb.py
│   ├── mostrar_documentos.py
│   ├── verificar_resultados.py
│   └── sincronizar_mongodb_neo4j.py
│
├── .gitignore
├── GUIA_CAPTURAS.md
├── README.md
└── requirements.txt
```

## Dataset utilizado

El dataset es sintético y reproducible. La generación produce:

| Entidad | Cantidad |
|---|---:|
| Usuarios | 50 |
| Productos | 120 |
| Reservas | 180 |
| Reseñas | 80 |

La base de MongoDB se llama `lightrip` y contiene las colecciones:

```text
usuarios
productos
reservas
resenas
```

## Requisitos

- Python 3.10 o superior.
- MongoDB Community Server.
- Neo4j Desktop.
- PowerShell, CMD o terminal de Visual Studio Code.

Conexiones locales utilizadas:

```text
MongoDB: mongodb://localhost:27017
Neo4j:   neo4j://127.0.0.1:7687
```

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/Anabela-Castellon/lightrip-ingenieria-datos-ii.git
cd lightrip-ingenieria-datos-ii
```

### 2. Crear y activar el entorno virtual

#### PowerShell

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

#### CMD

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## Ejecución de MongoDB

### 1. Generar el dataset

```powershell
py scripts\generar_dataset.py
```

Resultado esperado:

```text
Usuarios generados: 50
Productos generados: 120
Reservas generadas: 180
Reseñas generadas: 80
```

### 2. Validar el dataset

```powershell
py scripts\validar_dataset.py
```

Resultado esperado:

```text
Errores encontrados: 0
Dataset válido y listo para cargar.
```

### 3. Cargar MongoDB

```powershell
py scripts\cargar_mongodb.py
```

Resultado esperado:

```text
Base de datos: lightrip
Usuarios cargados: 50
Productos cargados: 120
Reservas cargadas: 180
Reseñas cargadas: 80
Índices creados correctamente.
```

El script elimina una base `lightrip` previa y vuelve a crearla. Esto permite repetir la carga sin duplicar documentos.

### 4. Mostrar documentos almacenados

```powershell
py scripts\mostrar_documentos.py
```

La salida muestra ejemplos de usuario, producto, reserva y reseña.

### 5. Ejecutar las consultas Q1 a Q7

```powershell
py scripts\verificar_resultados.py
```

Resultados obtenidos:

| Consulta | Resultado |
|---|---|
| Q1 | 6 productos de Camping disponibles en Bariloche |
| Q2 | 2 carpas con los atributos solicitados |
| Q3 | 5 productos disponibles y 1 excluido por superposición |
| Q4 | 3 reservas vigentes de `USR-001` |
| Q5 | 3 alquileres finalizados de `USR-001` |
| Q6 | Reputación 4.6 sobre 5 reseñas para `USR-002` |
| Q7 | `PROD-001` con 10 alquileres finalizados |

El script también genera:

```text
evidencias/resultados_mongodb.json
```

## Ejecución de Neo4j

1. Abrir Neo4j Desktop.
2. Iniciar la base local utilizada por el proyecto.
3. Verificar que el puerto Bolt sea `7687`.
4. Ejecutar las consultas Q8, Q9 y Q10 desde Neo4j Browser.

Resultados obtenidos:

| Consulta | Resultado |
|---|---|
| Q8 | 2 propietarios relacionados con `USR-001` |
| Q9 | 9 usuarios con propietarios en común |
| Q10 | 10 propietarios recomendados |

La segunda etapa de Q10 se ejecuta en MongoDB y recupera 24 productos disponibles pertenecientes a los propietarios recomendados.

## Flujo integrado entre MongoDB y Neo4j

El flujo implementado es:

```text
Reserva finalizada en MongoDB
        ↓
Procesamiento mediante Python
        ↓
Relación ALQUILO_A en Neo4j
        ↓
Consulta analítica sobre el grafo
```

### Configurar la contraseña de Neo4j

#### PowerShell

```powershell
$env:NEO4J_PASSWORD="TU_CONTRASEÑA"
```

#### CMD

```cmd
set NEO4J_PASSWORD=TU_CONTRASEÑA
```

La contraseña no debe incorporarse al código ni subirse al repositorio.

### Ejecutar la sincronización

```powershell
py scripts\sincronizar_mongodb_neo4j.py
```

Resultado de la primera ejecución:

```text
Reservas finalizadas pendientes: 90
Reservas nuevas aplicadas: 90
Reservas ya presentes: 0
Errores: 0
Nodos Usuario: 33
Relaciones ALQUILO_A: 88
Sincronización finalizada.
```

La cantidad de relaciones es menor que la cantidad de reservas porque varias operaciones entre el mismo cliente y propietario se consolidan en una sola relación.

### Verificación del caso `RES-001`

En Neo4j:

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

Resultado validado:

```text
USR-001 → USR-002
cantidad_operaciones: 2
categorias: ["Camping"]
reservas_procesadas: ["RES-001", "RES-006"]
```

En MongoDB:

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

La reserva debe presentar:

```text
estado: finalizada
sincronizada_neo4j: true
```

### Verificación de idempotencia

Después de volver a cargar MongoDB sin eliminar el grafo, se ejecutó nuevamente la sincronización.

Resultado obtenido:

```text
Reservas finalizadas pendientes: 90
Reservas nuevas aplicadas: 0
Reservas ya presentes: 90
Errores: 0
Nodos Usuario: 33
Relaciones ALQUILO_A: 88
```

Esto comprueba que las reservas ya procesadas no vuelven a incrementar los contadores ni generan relaciones duplicadas.

## Flujo completo de ejecución

```powershell
py scripts\generar_dataset.py
py scripts\validar_dataset.py
py scripts\cargar_mongodb.py
py scripts\mostrar_documentos.py
py scripts\verificar_resultados.py

$env:NEO4J_PASSWORD="12082013"
py scripts\sincronizar_mongodb_neo4j.py
```

Las consultas Q8 a Q10 se ejecutan desde Neo4j Browser.

## Evidencias

Las capturas deben guardarse dentro de:

```text
evidencias/
```

La guía detallada se encuentra en [GUIA_CAPTURAS.md](GUIA_CAPTURAS.md).

## Seguridad

No deben subirse al repositorio:

- `.venv/`
- `.env`
- Contraseñas.
- Caché de Python.
- Archivos temporales.

Estos elementos deben permanecer excluidos mediante `.gitignore`.
