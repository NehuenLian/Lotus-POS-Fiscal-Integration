import os
from contextlib import contextmanager

from dotenv import load_dotenv

from src.data_access.connection import DataBaseConnection


@contextmanager
def session_scope():
    load_dotenv()
    db_url = os.getenv("DB_URL")
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