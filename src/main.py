from fastapi import FastAPI
from src.api.routers.cliente.cliente_router import router as cliente_router
from src.api.routers.pix.pix_router import router as pix_router


app = FastAPI()


app.include_router(cliente_router, prefix="/cliente")
app.include_router(pix_router, prefix="/pix")
