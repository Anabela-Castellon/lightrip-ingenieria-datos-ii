# LighTrip — MongoDB

Este proyecto genera y carga la base MongoDB descrita en el informe final de
Ingeniería de Datos II.

## Resultado esperado

- 50 usuarios
- 120 productos
- 180 reservas
- 80 reseñas
- Base de datos: `lightrip`
- Colecciones: `usuarios`, `productos`, `reservas`, `resenas`

Los casos controlados permiten obtener:

- Q1: 6 productos de Camping disponibles en Bariloche.
- Q2: 2 carpas con capacidad mínima de 4 e impermeabilidad mínima de 3000 mm.
- Q3: 5 productos disponibles y 1 excluido (`PROD-002`).
- Q4: 3 reservas vigentes de `USR-001`.
- Q5: 3 alquileres finalizados de `USR-001`.
- Q6: reputación 4.6 para `USR-002`, calculada sobre 5 reseñas.
- Q7: `PROD-001` con 10 alquileres finalizados.

## 1. Requisitos

- Python 3.10 o superior.
- MongoDB Community ejecutándose localmente.
- MongoDB Compass para visualizar la base y tomar capturas.

La conexión predeterminada es:

```text
mongodb://localhost:27017
```

## 2. Abrir una terminal en la carpeta

En Windows, abrí PowerShell dentro de la carpeta `LighTrip_MongoDB`.

## 3. Crear el entorno virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Instalar PyMongo

```powershell
py -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Generar los archivos JSON

```powershell
py scripts\generar_dataset.py
```

Se crean:

- `data\usuarios.json`
- `data\productos.json`
- `data\reservas.json`
- `data\resenas.json`

Esta salida sirve para la Figura 2 del informe.

## 6. Validar el dataset

```powershell
py scripts\validar_dataset.py
```

El resultado esperado es:

```text
Errores encontrados: 0
Dataset válido y listo para cargar.
```

Esta salida también forma parte de la Figura 2.

## 7. Cargar MongoDB

Confirmá primero que el servicio de MongoDB esté iniciado y después ejecutá:

```powershell
py scripts\cargar_mongodb.py
```

El script elimina una base `lightrip` previa y vuelve a crearla. Esto permite
repetir la carga sin duplicar documentos.

Resultado esperado:

```text
Usuarios cargados: 50
Productos cargados: 120
Reservas cargadas: 180
Reseñas cargadas: 80
```

Esta salida sirve para la Figura 3.

## 8. Abrir la base en Compass

1. Abrí MongoDB Compass.
2. Conectate con `mongodb://localhost:27017`.
3. Presioná `Refresh`.
4. Abrí la base `lightrip`.
5. Verificá las colecciones:
   - `usuarios`
   - `productos`
   - `reservas`
   - `resenas`

Para la Figura 4, abrí uno o dos documentos de cada colección y expandí:

- `ubicacion`
- `especificaciones`
- `etiquetas`
- fechas
- campos numéricos

## 9. Ejecutar y verificar las consultas

Desde PowerShell:

```powershell
py scripts\verificar_resultados.py
```

El script ejecuta Q1 a Q7, muestra sus resultados y guarda:

```text
evidencias\resultados_mongodb.json
```

También podés ejecutar las consultas una por una desde:

```text
consultas\consultas_mongodb.js
```

## 10. Variables opcionales

Para utilizar otra conexión o nombre de base:

```powershell
$env:MONGO_URI="mongodb://localhost:27017"
$env:MONGO_DB="lightrip"
```
