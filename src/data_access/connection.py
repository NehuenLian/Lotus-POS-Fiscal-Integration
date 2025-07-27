from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data_access.database_tables import Base


class DataBaseConnection:
    _instance = None

    def __new__(cls, db_url: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_url: str):
        if not hasattr(self, 'engine'):
            self.db_url = db_url
            self.engine = create_engine(db_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = None

    def connect(self) -> None:
        if self.session is None:
            self.session = self.Session()

    def get_session(self):
        if self.session is None:
            self.connect()
        return self.session

    def close(self) -> None:
        if self.session:
            self.session.close()
            self.session = None
