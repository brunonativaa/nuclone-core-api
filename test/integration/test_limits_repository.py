from src.modules.limits.repository import LimitesRepository
from src.modules.limits.model import LimiteContaModel

def test_limits_repository_get_by_conta_and_update(db_session):
    repo = LimitesRepository(db_session)
    id_conta_teste = 101

    assert repo.get_by_conta(id_conta=id_conta_teste) is None

    novo_limite = LimiteContaModel(
        id_conta=id_conta_teste,
        limite_diario=1000.0,
        limite_noturno=300.0
    )
    limite_salvo = repo.update_limits(novo_limite)

    assert limite_salvo.id_conta == id_conta_teste
    assert limite_salvo.limite_diario == 1000.0

    limite_buscado = repo.get_by_conta(id_conta=id_conta_teste, for_update=False)
    assert limite_buscado is not None
    assert limite_buscado.id_conta == id_conta_teste

    limite_lock = repo.get_by_conta(id_conta=id_conta_teste, for_update=True)
    assert limite_lock is not None
    assert limite_lock.id_conta == id_conta_teste