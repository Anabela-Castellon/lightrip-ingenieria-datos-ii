# LighTrip — Ingeniería de Datos II

Repositorio del Trabajo Práctico Integrador de Ingeniería de Datos II.

La solución implementa la capa de datos de LighTrip mediante:

- MongoDB como base operativa principal.
- Python para generación, validación, carga y consultas.
- Neo4j como motor complementario para relaciones sociales e integración.

Este repositorio permite generar el dataset, cargar MongoDB y obtener las evidencias directamente desde la terminal. MongoDB Compass no es necesario.

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
├── scripts/
│   ├── generar_dataset.py
│   ├── validar_dataset.py
│   ├── cargar_mongodb.py
│   ├── mostrar_documentos.py
│   └── verificar_resultados.py
│
├── evidencias/
├── .gitignore
├── GUIA_CAPTURAS.md
├── README.md
└── requirements.txt
```

## Resultado esperado

La generación produce:

- 50 usuarios.
- 120 productos.
- 180 reservas.
- 80 reseñas.

La base creada se llama:

```text
lightrip
```

Sus colecciones son:

```text
usuarios
productos
reservas
resenas
```

## 1. Requisitos

- Python 3.10 o superior.
- MongoDB Community Server instalado.
- Servicio de MongoDB en ejecución.
- Terminal de Visual Studio Code, PowerShell o CMD.

MongoDB Compass es opcional y no se utiliza en esta guía.

## 2. Clonar el repositorio

```bash
git clone https://github.com/Anabela-Castellon/lightrip-ingenieria-datos-ii.git
cd lightrip-ingenieria-datos-ii
```

También se puede clonar mediante GitHub Desktop.

## 3. Crear el entorno virtual

### PowerShell

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### CMD

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

Cuando el entorno se encuentre activo, la terminal mostrará:

```text
(.venv)
```

## 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## 5. Verificar el servidor de MongoDB

### Desde PowerShell

```powershell
Get-Service MongoDB
```

El estado esperado es:

```text
Running
```

Si aparece detenido, abrir PowerShell como administrador y ejecutar:

```powershell
Start-Service MongoDB
```

### Desde Servicios de Windows

1. Presionar `Windows + R`.
2. Escribir `services.msc`.
3. Buscar `MongoDB Server`.
4. Seleccionar `Iniciar`.
5. Verificar que el estado sea `En ejecución`.

La conexión local utilizada por el proyecto es:

```text
mongodb://localhost:27017
```

## 6. Generar el dataset

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

Los archivos se guardan dentro de `data/`.

## 7. Validar el dataset

```powershell
py scripts\validar_dataset.py
```

Resultado esperado:

```text
Errores encontrados: 0
Dataset válido y listo para cargar.
```

## 8. Cargar MongoDB

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

El script elimina una base `lightrip` previa y la vuelve a crear. Esto permite repetir la ejecución sin duplicar documentos.

## 9. Mostrar documentos desde la terminal

```powershell
py scripts\mostrar_documentos.py
```

El script muestra ejemplos de:

- Usuario.
- Producto.
- Reserva.
- Reseña.

La salida incluye documentos embebidos, arreglos, fechas, identificadores y valores numéricos.

## 10. Ejecutar las consultas Q1 a Q7

```powershell
py scripts\verificar_resultados.py
```

El script ejecuta todas las consultas operativas de MongoDB y muestra:

```text
Q1: 6 productos.
Q2: 2 carpas.
Q3: 5 disponibles y 1 excluido: PROD-002.
Q4: 3 reservas vigentes.
Q5: 3 alquileres finalizados.
Q6: promedio 4.6 sobre 5 reseñas.
Q7: PROD-001 con 10 alquileres.
```

También genera:

```text
evidencias/resultados_mongodb.json
```

## 11. Flujo completo de ejecución

```powershell
py scripts\generar_dataset.py
py scripts\validar_dataset.py
py scripts\cargar_mongodb.py
py scripts\mostrar_documentos.py
py scripts\verificar_resultados.py
```

## 12. Evidencias

Las capturas se toman directamente desde la terminal y se guardan en:

```text
evidencias/
```

Nombres sugeridos:

```text
figura-02-generacion-validacion.png
figura-03-carga-mongodb.png
figura-04-documentos.png
figura-05-q1.png
figura-06-q2.png
figura-07-q3-disponibles.png
figura-08-q3-excluido.png
figura-09-q4.png
figura-10-q5.png
figura-11-q6.png
figura-12-q7.png
```

La guía detallada se encuentra en `GUIA_CAPTURAS.md`.

## 13. Seguridad y archivos ignorados

No deben subirse al repositorio:

- `.venv/`
- `.env`
- contraseñas
- archivos temporales
- caché de Python

Estos elementos se excluyen mediante `.gitignore`.
