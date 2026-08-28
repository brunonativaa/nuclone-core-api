from src.core.database import get_db


def test_get_db_yields_session():
    db_generator = get_db()
    session = next(db_generator)
    assert session is not None

    # Executa a limpeza (finally: db.close())
    try:
        next(db_generator)
    except StopIteration:
        pass
