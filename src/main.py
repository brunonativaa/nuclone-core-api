from fastapi import FastAPI
from src.core.database import Base, engine

from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel
from src.modules.account.model import ContaModel, SaldoContaModel, TransacaoModel
from src.modules.pix.model import KeyPixModel

from src.modules.customer.router import router as cliente_router
from src.modules.account.router import router as account_router
from src.modules.pix.router import router as pix_router


app = FastAPI(title="Nuclone Core API",
              description="API de serviços financeiros e transferências bancárias",
              version="1.0.0")

# create tables if not exist
Base.metadata.create_all(bind=engine)


app.include_router(cliente_router, prefix="/api/v1/customers")
app.include_router(account_router, prefix="/api/v1/accounts")
app.include_router(pix_router, prefix="/api/v1/pix")


@app.get('/', tags=["Health Check"])
def health_check():
    return {"status": "Ok", "menssage": "Nuclone API is running!"}
