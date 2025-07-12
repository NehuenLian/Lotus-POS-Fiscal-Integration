from contextlib import contextmanager

from src.data_access.connection import DataBaseConnection


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