import os
import uuid
from decimal import Decimal
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, patch
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

os.environ["RABBITMQ_USER"] = "admin"
os.environ["RABBITMQ_PASSWORD"] = "admin123"
os.environ["RABBITMQ_HOST"] = "localhost"

os.environ["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave_secreta_padrao_para_testes_unitarios_123")
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from src.main import app
from src.core.database import get_db, Base
from src.modules.account.model import ContaModel, SaldoContaModel, TipoContaEnum
from src.modules.limits.model import LimiteContaModel
from src.modules.customer.model import ClienteModel
from src.modules.pix.model import ChavePixModel


# -----------------------------------------------------------------------------
# Configuração Assíncrona do Banco em Memória
# -----------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# 1. Use explicitamente pytest_asyncio.fixture e garanta escopo de função
@pytest_asyncio.fixture(scope="function")
async def init_db():
    """Cria e destrói as tabelas a cada função de teste para garantir isolamento puro."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# 2. Defina o decorator correto do plugin assíncrono
@pytest_asyncio.fixture(scope="function")
async def db_session(init_db) -> AsyncGenerator[AsyncSession, None]:
    """Sessão assíncrona isolada para cada teste."""
    async with TestingSessionLocal() as session:
        yield session


# 3. Garanta que o override da dependência repasse a sessão corrente
@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP assíncrono conectado com override da sessão de BD de teste."""
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://testserver"
    ) as c:
        yield c
        
    app.dependency_overrides.clear()

@pytest.fixture
async def account_with_config_limits(db_session: AsyncSession):
    """
    Fixture que garante a criação atómica de uma conta bancária 
    juntamente com os seus perfis de limites diários e noturnos.
    """
    # 1. Criação da Conta Base
    cliente = ClienteModel(
        nome="Cliente de Teste",
        cpf="12551256587",
        email="teste.automacao@fintech.com",
        senha_hash="fake_hash_para_teste",
        pin_transacao_hash="152585", 
        sexo="M",
        data_nascimento = date(1997, 8, 15)
    )
    db_session.add(cliente)
    await db_session.commit()
    await db_session.refresh(cliente)

    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta="12345678-9",  # Garanta uma num_conta única se exigido pelo modelo
        tipo_conta=TipoContaEnum.PF,
        agencia="0001",
    )
    db_session.add(conta)
    await db_session.commit()
    await db_session.refresh(conta)

    saldo_inicial = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=Decimal("1500.00"),
        saldo_bloqueado=Decimal("0.00")
    )
    db_session.add(saldo_inicial)

    # 2. Provisionamento Obrigatório dos Limites de Transação
    limite = LimiteContaModel(
        id_conta=conta.id_conta,
        limite_diario=Decimal("10000.00"),
        limite_noturno=Decimal("600.00")
    )
    db_session.add(limite)

    await db_session.commit()
    await db_session.refresh(conta)

    return conta


@pytest.fixture(autouse=True)
def mock_rabbitmq_broker():
    with patch("src.core.broker.RabbitMQBroker.publish_event", new_callable=AsyncMock) as mock_publish:
        yield mock_publish


# -----------------------------------------------------------------------------
# Fixtures de Massa de Dados (Assíncronas e Sem Duplicidade)
# -----------------------------------------------------------------------------


@pytest.fixture
def valid_customer_data():
    uid = str(uuid.uuid4())[:8]
    return {
        "nome": f"Bruno Teste {uid}",
        "cpf": str(uuid.uuid4().int)[:11].zfill(11),
        "email": f"pytest_{uid}@email.com",
        "senha_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # "123456"
        "pin_transacao_hash": "1234",
        "sexo": "M",
        "data_nascimento": date(1997, 8, 15)
    }


@pytest.fixture
async def id_conta_origem(db_session: AsyncSession, valid_customer_data):
    cliente = ClienteModel(**valid_customer_data)
    db_session.add(cliente)
    await db_session.flush()

    uid = str(uuid.uuid4())[:5]
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid}-1",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    await db_session.flush()

    limite = LimiteContaModel(
        id_conta=conta.id_conta,
        limite_diario=Decimal("10000.00"),
        limite_noturno=Decimal("600.00")
    )
    db_session.add(limite)
    await db_session.commit()

    saldo = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=100.00,
        saldo_bloqueado=0.00,
        ultima_atualizacao=datetime.now(timezone.utc)
    )
    db_session.add(saldo)
    await db_session.flush()

    return conta.id_conta


@pytest.fixture
async def id_conta_destino(db_session: AsyncSession):
    uid = str(uuid.uuid4())[:8]
    dados_destino = {
        "nome": "Cliente Destino Teste",
        "cpf": str(uuid.uuid4().int)[:11].zfill(11),
        "email": f"destino_{uid}@email.com",
        "senha_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "pin_transacao_hash": "1234",
        "sexo": "F",
        "data_nascimento": date(1998, 1, 1)
    }
    cliente = ClienteModel(**dados_destino)
    db_session.add(cliente)
    await db_session.flush()

    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid[:5]}-2",
        agencia="0001",
        tipo_conta="PF"
    )
    db_session.add(conta)
    await db_session.flush()

    limite = LimiteContaModel(
        id_conta=conta.id_conta,
        limite_diario=Decimal("10000.00"),
        limite_noturno=Decimal("600.00")
    )
    
    db_session.add(limite)
    await db_session.commit()
    saldo = SaldoContaModel(
        id_conta=conta.id_conta,
        saldo_disponivel=0.00,
        saldo_bloqueado=0.00,
        ultima_atualizacao=datetime.now(timezone.utc)
    )
    db_session.add(saldo)
    await db_session.flush()

    return conta.id_conta


@pytest.fixture
async def chave_pix_origem(db_session: AsyncSession, id_conta_origem):
    chave = ChavePixModel(
        id_conta=id_conta_origem,
        tipo_chave="EMAIL",
        valor_chave="origem@email.com"
    )
    db_session.add(chave)
    await db_session.flush()
    return chave.valor_chave


@pytest.fixture
async def chave_pix_destino(db_session: AsyncSession, id_conta_destino):
    chave = ChavePixModel(
        id_conta=id_conta_destino,
        tipo_chave="EMAIL",
        valor_chave="destino@email.com"
    )
    db_session.add(chave)
    await db_session.flush()
    return chave.valor_chave