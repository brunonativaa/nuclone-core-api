from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.core.database import Base, engine
from src.modules.pix.model import ChavePixModel, TipoChavePixEnum
from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.ledger.models import TransacaoModel, TipoTransacaoEnum, StatusTransacaoEnum
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel
from src.modules.customer.router import router as cliente_router
from src.modules.account.router import router as account_router
from src.modules.pix.router import router as pix_router
from src.modules.auth.router import router as auth_router
from src.modules.ledger.router import router as ledger_router
from src.modules.limits.router import router as limits_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado na inicialização da aplicação
    Base.metadata.create_all(bind=engine)
    print("Iniciando serviços da API Bancária...")
    yield
    # Código de encerramento (se necessário)
    print("Encerrando serviços com segurança...")


app = FastAPI(
    title="Nuclone Core API",
    description="API de serviços financeiros e transferências bancárias",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    lifespan=lifespan

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir para os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router, prefix="/api/v1/customers")
app.include_router(account_router, prefix="/api/v1/accounts")
app.include_router(pix_router, prefix="/api/v1/pix")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(ledger_router, prefix="/api/v1")
app.include_router(limits_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "Ok", "message": "Nuclone API is running!"}
