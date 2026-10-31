import pytest
import random
from datetime import date
from decimal import Decimal
from src.modules.limits.repository import LimitesRepository
from src.modules.limits.model import LimiteContaModel
from src.modules.account.model import ContaModel, TipoContaEnum
from src.modules.customer.model import ClienteModel  # 👈 Necessário para a FK do cliente

@pytest.mark.asyncio
async def test_limits_repository_get_by_account_and_update(db_session):
    repo = LimitesRepository(db_session)
    id_conta_teste = 101
    id_cliente_teste = 1

    # 1. Garante a criação prévia do Cliente pai e da Conta pai no SQLite
    cliente_pai = ClienteModel(
        id_cliente=id_cliente_teste,
        nome="Cliente Teste Limites",
        cpf="12345678902",
        email="cliente_limites@email.com",
        senha_hash="fake_hash",
        pin_transacao_hash="1234",
        sexo="M",
        data_nascimento=date(1990, 1, 1)
    )
    conta_pai = ContaModel(
        id_conta=id_conta_teste,
        id_cliente=id_cliente_teste,
        num_conta="10101-1",
        tipo_conta=TipoContaEnum.PF,
        agencia="0001"
    )
    db_session.add_all([cliente_pai, conta_pai])
    await db_session.flush()

    assert await repo.get_by_conta(id_conta=id_conta_teste) is None

    # 2. Criação do modelo de limites com ID explícito (para o SQLite)
    novo_limite = LimiteContaModel(
        id_limite=random.randint(10000, 999999),  # 👈 Chave primária BigInteger explícita
        id_conta=id_conta_teste,
        limite_diario=Decimal("1000.0"),
        limite_noturno=Decimal("300.0")
    )
    limite_salvo = await repo.update_limits(novo_limite)

    assert limite_salvo.id_conta == id_conta_teste
    assert limite_salvo.limite_diario == Decimal("1000.0")

    limite_buscado = await repo.get_by_conta(id_conta=id_conta_teste, for_update=False)
    assert limite_buscado is not None
    assert limite_buscado.id_conta == id_conta_teste

    limite_lock = await repo.get_by_conta(id_conta=id_conta_teste, for_update=True)
    assert limite_lock is not None
    assert limite_lock.id_conta == id_conta_teste