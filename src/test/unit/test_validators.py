import pytest
from decimal import Decimal
from pydantic import ValidationError
from src.api.schemas.pix_schema import PixTransferInput
from src.api.schemas.customer_schema import ClienteCreateInput


# Calculator/Formatter Function

def test_validate_pix_amount_success_and_rounding():

    payload = PixTransferInput(
        id_conta_origem=1,
        id_conta_destino=2,
        valor=Decimal("10.556")
    )

    assert payload.valor == Decimal("10.56")


def test_validate_zero_or_negative_pix_value_generates_error():

    with pytest.raises(ValidationError) as exc_info:
        PixTransferInput(
            id_conta_origem=1,
            id_conta_destino=2,
            valor=Decimal("0.00")
        )

    assert "Valor da transação Pix deve ser maior que R$0,00" in str(
        exc_info.value)


# Verify CPF

@pytest.mark.unit
def test_validate_cpf_success():
    assert ClienteCreateInput.validar_cpf("123.456.789-09") == "12345678909"


@pytest.mark.unit
def test_validate_cpf_invalido():
    with pytest.raises(ValueError, match="CPF deve conter exatamente 11 dígitos "):
        ClienteCreateInput.validar_cpf("000")
