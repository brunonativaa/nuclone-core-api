import uuid
from datetime import date
from decimal import Decimal
from src.core.database import SessionLocal
from src.services.pix_service import PixService
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.conta_repository import ContaRepository

sufixo =str(uuid.uuid4().int)[:5]

def test_pix_service():

    db = SessionLocal()

    cliente_repo = ClienteRepository(db)
    conta_repo = ContaRepository(db)
    pix_service = PixService(db)

    # Criar cliente
    cliente = cliente_repo.create({
        "nome": "Teste Pix",
        "cpf": f"123456{sufixo}",
        "sexo": "M",
        "email": f"teste_{sufixo}pix@example.com",
        "senha": "123",
        "data_nascimento": date(1990, 1, 1)
    })

    # Criar conta origem
    conta_origem = conta_repo.criar_conta({
        "id_cliente": cliente.id_cliente,
        "num_conta": f"{sufixo}-6",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta_origem.id_conta)

    # Criar conta destino
    conta_destino = conta_repo.criar_conta({
        "id_cliente": cliente.id_cliente,
        "num_conta": f"{sufixo}-0",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta_destino.id_conta)

    # Adicionar saldo inicial na origem
    conta_repo.get_saldo(conta_origem.id_conta).saldo_disponivel = Decimal("100")
    db.commit()

    # Realizar PIX
    transacao = pix_service.realizar_pix(
        id_conta_origem=conta_origem.id_conta,
        id_conta_destino=conta_destino.id_conta,
        valor=Decimal("50.00")
    )

    # Validar transação criada
    assert transacao.id_transacao is not None

    # Validar saldos
    saldo_origem = conta_repo.get_saldo(conta_origem.id_conta)
    saldo_destino = conta_repo.get_saldo(conta_destino.id_conta)

    assert saldo_origem.saldo_disponivel == Decimal("50")
    assert saldo_destino.saldo_disponivel == Decimal("50")
