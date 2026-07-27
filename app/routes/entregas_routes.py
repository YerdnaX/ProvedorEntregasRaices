from datetime import datetime
from secrets import token_hex

from fastapi import APIRouter, HTTPException

from app.database import obtener_conexion
from app.schemas import CrearEntregaRequest, EntregaProvedor

router = APIRouter(prefix="/api", tags=["entregas"])


def convertir_entrega(fila) -> EntregaProvedor:
    return EntregaProvedor(
        idEntregaProvedor=fila["IdEntregaProvedor"],
        numeroOrden=fila["NumeroOrden"],
        trackingNumber=fila["TrackingNumber"],
        direccionEntrega=fila["DireccionEntrega"],
        estado=fila["Estado"],
        fechaCreacion=fila["FechaCreacion"],
    )


def generar_tracking_number() -> str:
    fecha = datetime.now().strftime("%Y%m%d")
    codigo = token_hex(3).upper()
    return f"RBX-{fecha}-{codigo}"


def obtener_por_numero_orden(cursor, numero_orden: int):
    cursor.execute(
        """
        SELECT
            IdEntregaProvedor,
            NumeroOrden,
            TrackingNumber,
            DireccionEntrega,
            Estado,
            FechaCreacion
        FROM ProvedorEntregas_Entregas
        WHERE NumeroOrden = %s
        """,
        (numero_orden,),
    )
    return cursor.fetchone()


@router.post("/entregas", response_model=EntregaProvedor)
def crear_entrega(datos: CrearEntregaRequest):
    direccion = datos.direccionEntrega.strip()
    if not direccion:
        raise HTTPException(status_code=400, detail="Debe indicar una direccion de entrega")

    with obtener_conexion() as conexion:
        cursor = conexion.cursor()

        entrega_existente = obtener_por_numero_orden(cursor, datos.numeroOrden)
        if entrega_existente is not None:
            return convertir_entrega(entrega_existente)

        for _ in range(5):
            tracking_number = generar_tracking_number()
            try:
                cursor.execute(
                    """
                    INSERT INTO ProvedorEntregas_Entregas (
                        NumeroOrden,
                        TrackingNumber,
                        DireccionEntrega,
                        Estado
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (datos.numeroOrden, tracking_number, direccion, "Registrada"),
                )
                conexion.commit()
                break
            except Exception:
                conexion.rollback()
        else:
            raise HTTPException(status_code=500, detail="No se pudo generar el tracking number")

        entrega = obtener_por_numero_orden(cursor, datos.numeroOrden)

    return convertir_entrega(entrega)


@router.get("/entregas/{tracking_number}", response_model=EntregaProvedor)
def obtener_entrega(tracking_number: str):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                IdEntregaProvedor,
                NumeroOrden,
                TrackingNumber,
                DireccionEntrega,
                Estado,
                FechaCreacion
            FROM ProvedorEntregas_Entregas
            WHERE TrackingNumber = %s
            """,
            (tracking_number,),
        )
        entrega = cursor.fetchone()

    if entrega is None:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")

    return convertir_entrega(entrega)
