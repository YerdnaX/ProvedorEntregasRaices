# Guia de integracion con Render

Esta guia explica como publicar `Provedor Entregas API` en Render como un Web Service.

## Configuracion en Render

Crear un nuevo servicio:

```txt
New
Web Service
Build and deploy from a Git repository
```

Configurar:

```txt
Name: provedor-entregas-raices
Environment: Python
Branch: master
Root Directory: dejar vacio
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

El repo incluye `runtime.txt` y `.python-version` con Python 3.12.8.

## Variables de entorno

```txt
DB_USER=usuario_sql
DB_PASSWORD=password_sql
DB_SERVER=tiusr15pl.cuc-carrera-ti.ac.cr
DB_DATABASE=tiusr15pl_ProvedoresRaicesBosque
DB_PORT=1433
PYTHON_VERSION=3.12.8
```

No agregar:

```txt
DB_DRIVER
DB_ENCRYPT
DB_TRUST_CERT
```

## Endpoints para probar

```bash
curl https://provedor-entregas-raices.onrender.com/api/health
curl -X POST https://provedor-entregas-raices.onrender.com/api/entregas -H "Content-Type: application/json" -d "{\"numeroOrden\":123,\"direccionEntrega\":\"Cartago, Costa Rica\"}"
```

## Integracion con backend principal

Cuando la API este publicada, actualizar el backend principal con:

```txt
PROVEDOR_ENTREGAS_API_URL=https://provedor-entregas-raices.onrender.com
```

No agregar una variable de timeout. El timeout queda fijo en el codigo del backend principal.
