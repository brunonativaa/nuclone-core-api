from datetime import date
import uuid
from src.modules.auth.repository import AuthRepository
from src.modules.customer.model import ClienteModel
from src.modules.account.model import ContaModel


def test_auth_repository_get_cliente_by_email(db_session):
    repo = AuthRepository(db_session)
    cliente = ClienteModel(
        nome="Teste Auth",
        cpf="12345678900",
        sexo="F",
        email="auth@test.com",
        senha_hash="hdieuhcdkd",
        pin_transacao_hash="528545",
        data_nascimento=date(1999, 2, 20)
    )

    db_session.add(cliente)
    db_session.commit()

    resultado = repo.get_cliente_by_email("auth@test.com")
    assert resultado is not None
    assert resultado.email == "auth@test.com"

    assert repo.get_cliente_by_email("nao_existe@test.com") is None

def test_auth_repository_get_account_by_cliente_id(db_session):
    repo = AuthRepository(db_session)
    cliente = ClienteModel( 
        nome="Teste Conta", 
            cpf="10987654321",
            sexo="M",
            email="conta@teste.com",
            senha_hash="kdhownjkcwpjk",
            pin_transacao_hash="123456",
            data_nascimento=date(1992, 1, 12)
)
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)


    uid = str(uuid.uuid4())[:5]
    conta = ContaModel(
        id_cliente=cliente.id_cliente,
        num_conta=f"000{uid}-1",
        agencia="0001",
        tipo_conta="PF"
    )

    db_session.add(conta)
    db_session.commit()
    db_session.refresh(conta)

    # 3. Executa a busca no repositorio
    resultado = repo.get_account_by_cliente_id(cliente.id_cliente)
    
    # Assertivas
    assert resultado is not None
    assert resultado.id_cliente == cliente.id_cliente

    # Teste de id inexistente
    assert repo.get_account_by_cliente_id(99999) is None