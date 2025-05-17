from contextlib import contextmanager
from src.database.connection import DataBaseConnection
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from src.utils.flags import FlagManager


@contextmanager
def session_scope():
    db_url = config("DATABASE_URL")
    connection = DataBaseConnection(db_url)
    session = connection.get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
