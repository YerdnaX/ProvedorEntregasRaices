from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.entregas_routes import router as entregas_router
from app.schemas import HealthResponse

app = FastAPI(title="Provedor Entregas API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health():
    return {
        "success": True,
        "message": "Provedor Entregas API funcionando correctamente",
    }


app.include_router(entregas_router)
