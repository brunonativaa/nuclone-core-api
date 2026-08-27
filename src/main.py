from fastapi import FastAPI
from src.modules.customer.customer_router import router as cliente_router
from src.modules.account.account_router import router as account_router
from src.modules.pix.pix_router import router as pix_router


app = FastAPI(title="Nuclone Core API",
              description="API de serviços financeiros e transferências bancárias",
              version="1.0.0")


<<<<<<< HEAD
app.include_router(cliente_router, prefix="/api/v1/customer")
app.include_router(account_router, prefix="/api/v1/accounts")
=======
app.include_router(cliente_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1")
>>>>>>> f609300 (refactor(arch): reorganizar estrutura do projeto para arquitetura modular (package-by-feature))
app.include_router(pix_router, prefix="/api/v1/pix")


@app.get('/', tags=["Health Check"])
def health_check():
    return {"status": "Ok", "menssage": "Nuclone API is running!"}
