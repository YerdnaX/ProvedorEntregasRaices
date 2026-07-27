from datetime import datetime
from pydantic import BaseModel


class CrearEntregaRequest(BaseModel):
    numeroOrden: int
    direccionEntrega: str


class EntregaProvedor(BaseModel):
    idEntregaProvedor: int
    numeroOrden: int
    trackingNumber: str
    direccionEntrega: str
    estado: str
    fechaCreacion: datetime


class HealthResponse(BaseModel):
    success: bool
    message: str
