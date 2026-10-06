import pytest
from sqlalchemy.exc import IntegrityError
from src.modules.pix.model import ChavePixModel, TipoChavePixEnum


async def test_rollback_fixture_recovery(db_session):

    with pytest.raises(IntegrityError):
        invalid_key = ChavePixModel(
            id_conta=None,
            tipo_chave=TipoChavePixEnum.EMAIL,
            valor_chave="teste@email.com"
        )

        db_session.add(invalid_key)
        await db_session.flush()

    await db_session.rollback()
