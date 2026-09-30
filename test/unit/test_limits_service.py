import pytest
from decimal import Decimal
from datetime import datetime, timezone
from unittest.mock import MagicMock
from src.modules.limits.service import LimitesService, LimitNotFoundException, ExceededLimitException
from src.modules.limits.schema import UpdateLimiteSchema
from src.modules.limits.model import LimiteContaModel

@pytest.fixture
def mock_repos():
    limits_repo = MagicMock()
    ledger_repo = MagicMock()
    return limits_repo, ledger_repo


def  test_validate_and_use_account_limit_not_found(mock_repos):
    limits_repo, ledger_repo = mock_repos
    limits_repo.get_by_conta.return_value = None
    service = LimitesService(limits_repo, ledger_repo)

    with pytest.raises(LimitNotFoundException):
        service.validar_e_consumir_limite(id_conta=1, valor=Decimal("100.00"))

def test_validate_and_consume_limit_exceeded(mock_repos):
    limits_repo , ledger_repo = mock_repos

    # Configura limite de R$ 500
    limite_config = LimiteContaModel(id_conta=1, limite_diario=Decimal("500.00"), limite_noturno=Decimal("200.00"))
    limits_repo.get_by_conta.return_value = limite_config
    
    # Simula gasto acumulado de R$ 450
    ledger_repo.get_total_gasto_janela.return_value = Decimal("450.00")
    
    service = LimitesService(limits_repo, ledger_repo)

    # Tenta transação de R$ 100 (supera o disponível de R$ 50)
    with pytest.raises(ExceededLimitException) as exc_info:
        service.validar_e_consumir_limite(id_conta=1, valor=Decimal("100.00"))
    
    assert exc_info.value.disponivel == Decimal("50.00")

def test_validate_and_use_limit_success(mock_repos):
    limits_repo, ledger_repo = mock_repos
    
    limite_config = LimiteContaModel(id_conta=1, limite_diario=Decimal("1000.00"), limite_noturno=Decimal("500.00"))
    limits_repo.get_by_conta.return_value = limite_config
    ledger_repo.get_total_gasto_janela.return_value = Decimal("100.00")
    
    service = LimitesService(limits_repo, ledger_repo)
    
    resultado = service.validar_e_consumir_limite(id_conta=1, valor=Decimal("200.00"))
    assert resultado is True

def test_get_status_limits_success(mock_repos):
    limits_repo, ledger_repo = mock_repos
    
    limite_config = LimiteContaModel(id_conta=1, limite_diario=Decimal("1000.00"), limite_noturno=Decimal("300.00"))
    limits_repo.get_by_conta.return_value = limite_config
    ledger_repo.get_total_gasto_janela.side_effect = [Decimal("150.00"), Decimal("0.00")]
    
    service = LimitesService(limits_repo, ledger_repo)
    status = service.obter_status_limites(id_conta=1)

    assert status["id_conta"] == 1
    assert status["limite_diario"] == Decimal("1000.00")
    assert status["limite_diario_utilizado"] == Decimal("150.00")

def test_update_limits_success(mock_repos):
    limits_repo, ledger_repo = mock_repos
    
    limite_config = LimiteContaModel(id_conta=1, limite_diario=Decimal("1000.00"), limite_noturno=Decimal("300.00"))
    limits_repo.get_by_conta.return_value = limite_config
    ledger_repo.get_total_gasto_janela.return_value = Decimal("0.00")
    
    service = LimitesService(limits_repo, ledger_repo)
    
    payload = UpdateLimiteSchema(novo_limite_diario=Decimal("2000.00"), novo_limite_noturno=None)
    res = service.atualizar_limites(id_conta=1, payload=payload)

    assert limits_repo.update_limits.called
    assert limite_config.limite_diario == Decimal("2000.00")