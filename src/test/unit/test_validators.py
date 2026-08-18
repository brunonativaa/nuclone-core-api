import pytest
from src.api.schemas.customer_schema import ClienteCreateInput


@pytest.mark.unit
def test_validar_cpf_success():
    assert ClienteCreateInput.validar_cpf("123.456.789-09") == "12345678909"


@pytest.mark.unit
def test_validar_cpf_invalido():
    with pytest.raises(ValueError, match="CPF deve conter exatamente 11 dígitos "):
        ClienteCreateInput.validar_cpf("000")
