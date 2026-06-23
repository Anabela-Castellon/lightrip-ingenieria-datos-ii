// Ejecutar desde mongosh o desde el shell integrado de MongoDB Compass.
use("lightrip");

// Q1. Búsqueda por categoría y ubicación.
db.productos.find(
  {
    categoria: "Camping",
    "ubicacion.ciudad": "Bariloche",
    estado: "disponible"
  },
  {
    _id: 0,
    producto_id: 1,
    nombre: 1,
    categoria: 1,
    ubicacion: 1,
    precio_por_dia: 1
  }
).sort({ producto_id: 1 });

// Q2. Filtro por atributos específicos.
db.productos.find(
  {
    categoria: "Camping",
    subcategoria: "Carpas",
    "especificaciones.capacidad": { $gte: 4 },
    "especificaciones.impermeabilidad_mm": { $gte: 3000 },
    estado: "disponible"
  },
  {
    _id: 0,
    producto_id: 1,
    nombre: 1,
    especificaciones: 1,
    precio_por_dia: 1
  }
).sort({ producto_id: 1 });

// Q3. Disponibilidad por fechas.
const inicio = ISODate("2026-07-10T00:00:00Z");
const fin = ISODate("2026-07-15T00:00:00Z");

db.productos.aggregate([
  {
    $match: {
      categoria: "Camping",
      "ubicacion.ciudad": "Bariloche",
      estado: "disponible"
    }
  },
  {
    $lookup: {
      from: "reservas",
      let: { productoId: "$producto_id" },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [
                { $eq: ["$producto_id", "$$productoId"] },
                {
                  $in: [
                    "$estado",
                    ["pendiente", "confirmada", "activa"]
                  ]
                },
                { $lt: ["$fecha_inicio", fin] },
                { $gt: ["$fecha_fin", inicio] }
              ]
            }
          }
        }
      ],
      as: "reservas_bloqueantes"
    }
  },
  {
    $match: {
      reservas_bloqueantes: { $size: 0 }
    }
  },
  {
    $project: {
      _id: 0,
      producto_id: 1,
      nombre: 1,
      categoria: 1,
      ubicacion: 1,
      precio_por_dia: 1
    }
  },
  { $sort: { producto_id: 1 } }
]);

// Evidencia complementaria de Q3: reserva bloqueante.
db.reservas.find(
  {
    producto_id: "PROD-002",
    estado: { $in: ["pendiente", "confirmada", "activa"] },
    fecha_inicio: { $lt: fin },
    fecha_fin: { $gt: inicio }
  },
  {
    _id: 0,
    reserva_id: 1,
    producto_id: 1,
    estado: 1,
    fecha_inicio: 1,
    fecha_fin: 1
  }
);

// Q4. Reservas activas de USR-001.
db.reservas.find(
  {
    usuario_solicitante_id: "USR-001",
    estado: { $in: ["pendiente", "confirmada", "activa"] }
  },
  {
    _id: 0,
    reserva_id: 1,
    producto_id: 1,
    fecha_inicio: 1,
    fecha_fin: 1,
    precio_total: 1,
    estado: 1
  }
).sort({ fecha_inicio: 1 });

// Q5. Historial de alquileres.
db.reservas.aggregate([
  {
    $match: {
      usuario_solicitante_id: "USR-001",
      estado: "finalizada"
    }
  },
  {
    $lookup: {
      from: "productos",
      localField: "producto_id",
      foreignField: "producto_id",
      as: "producto"
    }
  },
  { $unwind: "$producto" },
  {
    $project: {
      _id: 0,
      reserva_id: 1,
      fecha_inicio: 1,
      fecha_fin: 1,
      precio_total: 1,
      producto_id: "$producto.producto_id",
      producto: "$producto.nombre",
      categoria: "$producto.categoria"
    }
  },
  { $sort: { fecha_fin: -1 } }
]);

// Q6. Cálculo de reputación.
db.resenas.aggregate([
  {
    $match: {
      usuario_destinatario_id: "USR-002"
    }
  },
  {
    $group: {
      _id: "$usuario_destinatario_id",
      reputacion_promedio: { $avg: "$puntaje" },
      cantidad_resenas: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      usuario_id: "$_id",
      reputacion_promedio: {
        $round: ["$reputacion_promedio", 2]
      },
      cantidad_resenas: 1
    }
  }
]);

// Q7. Productos con mayor demanda.
db.reservas.aggregate([
  { $match: { estado: "finalizada" } },
  {
    $group: {
      _id: "$producto_id",
      cantidad_alquileres: { $sum: 1 },
      ingresos_generados: { $sum: "$precio_total" }
    }
  },
  {
    $sort: {
      cantidad_alquileres: -1,
      ingresos_generados: -1
    }
  },
  { $limit: 10 },
  {
    $lookup: {
      from: "productos",
      localField: "_id",
      foreignField: "producto_id",
      as: "producto"
    }
  },
  { $unwind: "$producto" },
  {
    $project: {
      _id: 0,
      producto_id: "$_id",
      nombre: "$producto.nombre",
      categoria: "$producto.categoria",
      cantidad_alquileres: 1,
      ingresos_generados: 1
    }
  }
]);
