from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.broker import broker


from src.core.database import Base, engine
from src.modules.pix.model import ChavePixModel, TipoChavePixEnum
from src.modules.account.model import ContaModel, SaldoContaModel
from src.modules.ledger.model import TransacaoModel, TipoTransacaoEnum, StatusTransacaoEnum
from src.modules.customer.model import ClienteModel, EnderecoModel, TelefoneModel
from src.modules.customer.router import router as cliente_router
from src.modules.account.router import router as account_router
from src.modules.pix.router import router as pix_router
from src.modules.auth.router import router as auth_router
from src.modules.ledger.router import router as ledger_router
from src.modules.limits.router import router as limits_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup: Executa o DDL de criação de tabelas de forma assíncrona ---
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Banco de dados inicializado com sucesso!")
   
    try:
        await broker.declare_topology(
            exchange_name="nuclone.pix.exchange",
            queue_name="pix.processing.queue",
            routing_key="pix.solicitado"
        )
        
        print("Topologia do RabbitMQ declarada e vinculada com sucesso!")
    
    except Exception as e:
        # Em produção, tratamos falhas de infraestrutura para que o app suba ou falhe de forma controlada
        print(f"[AVISO CRÍTICO] Não foi possível conectar ao RabbitMQ no boot: {e}")
        # Dependendo da criticidade, você pode optar por relançar o erro (raise e) se o mensageiro for obrigatório

    yield  # --- A aplicação roda aqui atendendo requisições ---

    # --- 3. Shutdown: Encerra conexões ativas com segurança ---
    print("Encerrando serviços com segurança...")

    if broker._connection and not broker._connection.is_closed:
        await broker._connection.close()
        print("Conexão com o RabbitMQ encerrada.")

    await engine.dispose()

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

app.include_router(cliente_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1")
app.include_router(pix_router, prefix="/api/v1/pix")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(ledger_router, prefix="/api/v1")
app.include_router(limits_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "Ok", "message": "Nuclone API is running!"}
