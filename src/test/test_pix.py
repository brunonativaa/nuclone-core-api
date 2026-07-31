import uuid
from decimal import Decimal
from datetime import date
from src.core.database import SessionLocal
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.conta_repository import ContaRepository
from src.repositories.pix_repository import PixRepository


def test_fluxo_pix():
    db = SessionLocal()

    cliente_repo = ClienteRepository(db)
    conta_repo = ContaRepository(db)
    pix_repo = PixRepository(db)

    # Gera sufixo único para evitar erros de UniqueViolation no banco
    sufixo_unico = str(uuid.uuid4().int)[:5]

    # 1. Cria cliente
    cliente = cliente_repo.create({
        "nome": "Shi-Ha",
        "cpf": f"123569{sufixo_unico}",
        "sexo": "F",
        "email": f"Shiha_{sufixo_unico}@apple.com",
        "senha": "1565584",
        "data_nascimento": date(1998, 1, 10)
    })

    # 2. Cria conta de origem e inicializa saldo
    conta_origem = conta_repo.create({
        "id_cliente": cliente.id_cliente,
        "num_conta": f"{sufixo_unico}-1",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta_origem.id_conta)

    # 3. Cria conta de destino e inicializa saldo
    conta_destino = conta_repo.create({
        "id_cliente": cliente.id_cliente,
        "num_conta": f"{sufixo_unico}-2",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta_destino.id_conta)

    # 4. Adiciona saldo na conta de origem (ex: R$ 100,00)
    pix_repo.atualizar_saldo(conta_origem.id_conta, 100.0)

    # 5. Executa a transferência PIX de R$ 50,00
    dados_transacao = {
        "id_conta_origem": conta_origem.id_conta,
        "id_conta_destino": conta_destino.id_conta,
        "valor": Decimal("50.0"),
        "tipo_transacao": "PIX"  # Ajuste os campos conforme o seu TransacaoModel
    }

    transacao = pix_repo.transferir_pix(
        id_conta_origem=conta_origem.id_conta,
        id_conta_destino=conta_destino.id_conta,
        valor=Decimal("50.0"),
        dados_transacao=dados_transacao
    )

    # 6. Asserts para validar se deu tudo certo
    assert transacao is not None
    assert transacao.id_transacao is not None
