def test_fluxo_pix():

    from datetime import date
    from src.core.database import SessionLocal
    from src.repositories.cliente_repository import ClienteRepository
    from src.repositories.conta_repository import ContaRepository
    from src.repositories.pix_repository import PixRepository

    db = SessionLocal()

    cliente_repo = ClienteRepository(db)
    conta_repo = ContaRepository(db)
    pix_repo = PixRepository(db)

    cliente = cliente_repo.create({
        "nome": "Hi-man",
        "cpf": "12356985999",
        "sexo": "M",
        "email": "himan_unico@apple.com",
        "senha": "1565584",
        "data_nascimento": date(1998, 1, 10)
    })
    conta = conta_repo.create({
        "id_cliente": cliente.id_cliente,
        "num_conta": "12225-6",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta.id_conta)

    # Conta destino
    conta_destino = conta_repo.create({
        "id_cliente": cliente.id_cliente,
        "num_conta": "98765-0",
        "tipo_conta": "PF",
        "agencia": "0001"
    })
    conta_repo.criar_saldo(conta_destino.id_conta)

    # PIX
    pix_repo.debitar(conta.id_conta, 50)
    pix_repo.creditar(conta_destino.id_conta, 50)

    transacao = pix_repo.registrar_transacao({
        "id_conta_origem": conta.id_conta,
        "id_conta_destino": conta_destino.id_conta,
        "valor": 50,
        "tipo": "PIX"
    })

    print("Transação criada:", transacao.id_transacao)
    print("Saldo origem:", conta_repo.get_saldo(
        conta.id_conta).saldo_disponivel)
    print("Saldo destino:", conta_repo.get_saldo(
        conta_destino.id_conta).saldo_disponivel)
