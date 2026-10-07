from src.core.database import get_db


async def test_get_db_yields_session():
    db_generator = get_db()
    session = await anext(db_generator)
    assert session is not None

    # Executa a limpeza (finally: db.close())
    try:
        await anext(db_generator)
    except StopAsyncIteration:
        pass
