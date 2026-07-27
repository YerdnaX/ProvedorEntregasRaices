# Provedor Entregas API

API fake en Python con FastAPI para simular un socio comercial de entregas.

Cuando el backend principal crea una compra con entrega a domicilio, esta API genera un `trackingNumber` unico para el numero de orden recibido.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copiar `.env.example` a `.env` y completar las credenciales reales de SQL Server.

Esta API usa `pymssql`, por lo que no necesita configurar `DB_DRIVER` ni instalar un driver ODBC en Windows.

## Base de datos

La base de datos usada por los provedores es:

```txt
tiusr15pl_ProvedoresRaicesBosque
```

Ejecutar primero:

```txt
database/crear_tablas.sql
database/datos_prueba.sql
```

## Ejecutar

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

## Pruebas

```bash
curl http://localhost:8003/api/health
curl http://localhost:8003/api/entregas
curl -X POST http://localhost:8003/api/entregas -H "Content-Type: application/json" -d "{\"numeroOrden\":123,\"direccionEntrega\":\"Cartago, Costa Rica\"}"
curl http://localhost:8003/api/entregas/RBX-20260727-DEMO01
```
