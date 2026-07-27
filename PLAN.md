# Plan - Provedor Entregas API

## Objetivo

Crear una API fake en Python con FastAPI que simule un socio comercial de entregas a domicilio.

Cuando el usuario confirme una compra con `metodoEntrega = 'Domicilio'`, el backend principal consultara este provedor para generar un tracking number unico asociado a esa orden.

La app movil no consumira directamente esta API.

## Alcance inicial

Este plan cubre solamente `provedores/provedor-entregas`.

La primera version debe permitir:

1. Registrar una entrega para una compra.
2. Generar un `trackingNumber` unico.
3. Guardar la relacion entre numero de orden generado por el backend principal y tracking number.
4. Consultar una entrega por tracking number.
5. Consultar todas las entregas registradas.
6. Permitir que el backend principal devuelva el tracking a la app.
7. Permitir que la app muestre una pantalla de confirmacion para compras a domicilio.

No se implementara seguimiento real de paquetes.
No se integrara con mapas.
No se calculara costo real de envio.
No se notificara por correo o SMS.

## Tecnologia

El proyecto usara:

- Python.
- FastAPI.
- Uvicorn.
- SQL Server.
- `pymssql`.
- Variables de entorno para conexion.

No usar `pyodbc`.
No usar `DB_DRIVER`.
No usar `DB_ENCRYPT`.
No usar `DB_TRUST_CERT`.

Regla importante para consultas con parametros en `pymssql`:

```py
cursor.execute(
    "SELECT * FROM ProvedorEntregas_Entregas WHERE TrackingNumber = %s",
    (tracking_number,),
)
```

No usar `?` como placeholder.

## Estructura propuesta

```txt
provedores/
└── provedor-entregas/
    ├── PLAN.md
    ├── README.md
    ├── RENDER.md
    ├── requirements.txt
    ├── runtime.txt
    ├── .python-version
    ├── .env.example
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── schemas.py
    │   └── routes/
    │       └── entregas_routes.py
    └── database/
        ├── crear_tablas.sql
        └── datos_prueba.sql
```

## Base de datos

Usar la misma base de datos de provedores:

```txt
tiusr15pl_ProvedoresRaicesBosque
```

Todas las tablas de este provedor deben iniciar con:

```txt
ProvedorEntregas_
```

Tabla principal:

```txt
ProvedorEntregas_Entregas
```

Campos:

```txt
IdEntregaProvedor INT IDENTITY(1,1) PRIMARY KEY
NumeroOrden       INT NOT NULL
TrackingNumber    VARCHAR(50) NOT NULL UNIQUE
DireccionEntrega  VARCHAR(300) NOT NULL
Estado            VARCHAR(50) NOT NULL
FechaCreacion     DATETIME NOT NULL DEFAULT GETDATE()
```

Notas:

- `NumeroOrden` sera el mismo `IdCompra` generado por el backend principal al realizar la compra.
- El provedor no debe inventar ni recalcular el numero de orden.
- El provedor solo debe recibirlo, guardarlo y devolverlo en sus respuestas.
- `TrackingNumber` sera generado por el provedor. Ejemplo: `RBX-20260727-8F3A2C`.
- No habra foreign key hacia la base principal.
- No guardar datos sensibles.
- No guardar credenciales en el codigo.

## Endpoints propuestos

Base local:

```txt
http://localhost:8003
```

### Health

```txt
GET /api/health
```

Respuesta:

```json
{
  "success": true,
  "message": "Provedor Entregas API funcionando correctamente"
}
```

### Crear entrega

```txt
POST /api/entregas
```

Request:

```json
{
  "numeroOrden": 123,
  "direccionEntrega": "Cartago, Costa Rica, 200 metros norte de la iglesia"
}
```

Respuesta exitosa:

```json
{
  "idEntregaProvedor": 1,
  "numeroOrden": 123,
  "trackingNumber": "RBX-20260727-8F3A2C",
  "direccionEntrega": "Cartago, Costa Rica, 200 metros norte de la iglesia",
  "estado": "Registrada",
  "fechaCreacion": "2026-07-27T10:30:00"
}
```

Regla de idempotencia:

- Si ya existe una entrega para el mismo `NumeroOrden`, retornar la entrega existente.
- No generar multiples tracking numbers para la misma compra.

### Consultar por tracking

### Consultar todas las entregas

```txt
GET /api/entregas
```

Respuesta:

```json
[
  {
    "idEntregaProvedor": 1,
    "numeroOrden": 123,
    "trackingNumber": "RBX-20260727-8F3A2C",
    "direccionEntrega": "Cartago, Costa Rica, 200 metros norte de la iglesia",
    "estado": "Registrada",
    "fechaCreacion": "2026-07-27T10:30:00"
  }
]
```

### Consultar por tracking

```txt
GET /api/entregas/{trackingNumber}
```

Respuesta exitosa:

```json
{
  "idEntregaProvedor": 1,
  "numeroOrden": 123,
  "trackingNumber": "RBX-20260727-8F3A2C",
  "direccionEntrega": "Cartago, Costa Rica, 200 metros norte de la iglesia",
  "estado": "Registrada",
  "fechaCreacion": "2026-07-27T10:30:00"
}
```

Si no existe:

```json
{
  "error": "Entrega no encontrada"
}
```

Codigo HTTP:

```txt
404
```

## Integracion con backend principal

Variable de entorno:

```txt
PROVEDOR_ENTREGAS_API_URL=http://localhost:8003
```

No agregar variable de timeout.

Timeout fijo en codigo:

```txt
5000 ms
```

Flujo esperado en `POST /api/compras`:

1. Validar datos de compra.
2. Si `metodoEntrega = 'Domicilio'`, resolver `direccionFinal`.
3. Crear compra en `Compras` y obtener `IdCompra`, que se usara como `numeroOrden`.
4. Crear detalle de compra.
5. Completar carrito.
6. Si `metodoEntrega = 'Domicilio'`, llamar al provedor:

```txt
POST {PROVEDOR_ENTREGAS_API_URL}/api/entregas
```

Payload:

```json
{
  "numeroOrden": 123,
  "direccionEntrega": "Cartago, Costa Rica, 200 metros norte de la iglesia"
}
```

7. Responder a la app:

Compra en tienda:

```json
{
  "success": true,
  "idCompra": 123,
  "trackingNumber": null
}
```

Compra a domicilio:

```json
{
  "success": true,
  "idCompra": 123,
  "trackingNumber": "RBX-20260727-8F3A2C"
}
```

Si el provedor falla:

- No romper la compra si ya fue registrada correctamente.
- Responder `trackingNumber: null`.
- La app debe mostrar confirmacion de compra, pero indicar que no se pudo generar tracking.

## Integracion con app movil

La app seguira consumiendo solo el backend principal.

Pantalla afectada:

```txt
app/src/app/checkout.tsx
```

Despues de confirmar compra:

- Siempre debe navegar a la misma pantalla nueva de confirmacion.
- Si `metodoEntrega = 'Tienda'`, no debe mostrar tracking number.
- Si `metodoEntrega = 'Domicilio'`, debe mostrar tracking number si existe.

Pantalla nueva sugerida:

```txt
app/src/app/compra-confirmada.tsx
```

La pantalla debe:

- Mostrar mensaje de compra confirmada.
- Mostrar el numero de orden, que sera el mismo `IdCompra`.
- Mostrar el tracking number solo si `metodoEntrega = 'Domicilio'` y existe.
- Mostrar mensaje claro si `metodoEntrega = 'Domicilio'` y el tracking no pudo generarse.
- No mostrar seccion de tracking si `metodoEntrega = 'Tienda'`.
- No permitir navegar hacia atras.
- Tener una accion visible para volver al inicio.

Accion:

```txt
Volver al inicio
```

Debe usar:

```ts
router.replace('/(tabs)')
```

No usar:

```ts
router.back()
```

## Criterios de aceptacion

La implementacion se considerara lista cuando:

- `provedores/provedor-entregas` tenga estructura FastAPI completa.
- `GET /api/health` responda correctamente.
- `POST /api/entregas` genere un tracking unico.
- `POST /api/entregas` sea idempotente por `NumeroOrden`.
- `GET /api/entregas/{trackingNumber}` consulte una entrega existente.
- El backend principal llame al provedor solo para `metodoEntrega = 'Domicilio'`.
- El backend principal devuelva `trackingNumber` en `POST /api/compras`.
- La app muestre la misma pantalla de confirmacion para compras en tienda y a domicilio.
- La pantalla no muestre tracking para compras en tienda.
- La pantalla de confirmacion no permita navegar hacia atras.
- La pantalla tenga accion para volver al inicio.

## Pruebas manuales esperadas

Comandos curl sugeridos para el provedor:

```bash
curl http://localhost:8003/api/health
curl http://localhost:8003/api/entregas
curl -X POST http://localhost:8003/api/entregas ^
  -H "Content-Type: application/json" ^
  -d "{\"numeroOrden\":123,\"direccionEntrega\":\"Cartago, Costa Rica\"}"
curl http://localhost:8003/api/entregas/RBX-20260727-8F3A2C
```

Comando curl sugerido para el backend principal:

```bash
curl -X POST http://localhost:3000/api/compras ^
  -H "Content-Type: application/json" ^
  -d "{\"idUsuario\":1,\"metodoEntrega\":\"Domicilio\",\"direccionEntrega\":\"Cartago, Costa Rica\"}"
```

## Pendiente para despues de aprobar este plan

1. Crear archivos de la API en `provedores/provedor-entregas`.
2. Crear scripts SQL del provedor.
3. Actualizar `backend/src/controllers/compras.controller.js`.
4. Actualizar `backend/.env.example`.
5. Actualizar `app/src/features/compras/services/compraService.ts`.
6. Crear `app/src/app/compra-confirmada.tsx`.
7. Probar sintaxis backend y Python.
8. Probar TypeScript de app.
