from fastapi import FastAPI
from src.api.routers.customer_router import router as cliente_router
from src.api.routers.account_router import router as account_router
from src.api.routers.pix_router import router as pix_router


app = FastAPI(title="Nuclone Core API",
              description="API de serviços financeiros e transferências bancárias",
              version="1.0.0")


app.include_router(cliente_router)
app.include_router(account_router)
app.include_router(pix_router)


@app.get('/', tags=["Health Check"])
def health_check():
    return {"status": "Ok", "menssage": "Nuclone API is running!"}
