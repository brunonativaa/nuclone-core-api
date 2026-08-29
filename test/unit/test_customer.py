import pytest
from src.modules.customer.service import (
    ClienteService,
    ClienteJaExisteException,
    ClienteNaoEncontradoException
)


def test_create_customer_duplicate_cpf_should_fail(db_session, valid_customer_data):
    """Testa a regra de negócio que impede o cadastro de CPFs duplicados.
    Espera-se que a exceção customizada ClienteJaExisteException seja lançada."""

    service = ClienteService(db_session)
    service.create_customer(valid_customer_data)

    duplicate_data = valid_customer_data.copy()
    duplicate_data["email"] = "other_email@email.com"

    with pytest.raises(ClienteJaExisteException):
        service.create_customer(duplicate_data)


def test_get_customer_by_non_existing_id_should_fail(db_session):
    """Testa a busca por um ID inexistente no banco.
    Espera-se que a exceção ClienteNaoEncontradoException seja capturada.
    """

    service = ClienteService(db_session)

    with pytest.raises(ClienteNaoEncontradoException):
        service.get_by_id(id_cliente=9999999)
