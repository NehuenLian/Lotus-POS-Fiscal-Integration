from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.flags import FlagManager
from sqlalchemy.exc import ArgumentError
from src.exceptions import InvalidDatabaseURLError


class DataBaseConnection:
    _instance = None

    def __new__(cls, db_url: str):
        if not cls._instance:
            cls._flag = FlagManager()
            cls._instance = super(DataBaseConnection, cls).__new__(cls)
            cls._instance.db_url = db_url
            try:
                cls._instance.engine = create_engine(db_url)
                cls._instance.Session = sessionmaker(bind=cls._instance.engine)
                cls._instance.session = None
                cls._flag.connection_exists = True
            except ArgumentError as e:
                cls._flag.connection_exists = False
                raise InvalidDatabaseURLError(db_url, original_exception=e)

        return cls._instance

    def connect(self):
        try:
            self.session = self.Session()
            self._flag.connection_exists = True
        except:
            self._flag.connection_exists = False

    def get_session(self):
        self.connect()
        return self.session

    def close(self):
        try:
            self.session.close()
            self.session = None
            self._flag.connection_exists = False
        except:
            self._flag.connection_exists = False