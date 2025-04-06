from contextlib import contextmanager

from src.database.connection import DataBaseConnection


@contextmanager
def session_scope(connection: DataBaseConnection):
    session = connection.get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()