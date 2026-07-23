from fastapi import FastAPI
from src.modules.cliente.cliente_router import router as cliente_router
from src.modules.pix.pix_router import router as pix_router


app = FastAPI(title="Nuclone API", version="1.0.0")

@app.get("/")
def home():
    return {"menssage": "API Nuclone operando com sucesso!"}

app.include_router(cliente_router, prefix="/cliente")
app.include_router(pix_router, prefix="/pix")
