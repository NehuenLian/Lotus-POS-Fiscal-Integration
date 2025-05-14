from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBaseConnection:
    _instance = None

    def __new__(cls, db_url: str):
        if not cls._instance: # Singleton
            cls._instance = super(DataBaseConnection, cls).__new__(cls)
            cls._instance.db_url = db_url
            cls._instance.engine = create_engine(db_url)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            cls._instance.session = None

        return cls._instance

    def connect(self):
        if not self.session:
            self.session = self.Session()
            print("conexion establecida")

    def get_session(self):
        if not self.session:
            self.connect()
            print("Conexión exitosa src/database/connection.py")
        return self.session

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

