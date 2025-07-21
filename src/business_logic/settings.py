from src.data_access.connection import DataBaseConnection
from pathlib import Path


class SettingsManagement:
    def __init__(self):
        pass

    def connect_to_db(self, db_url: str) -> None:
        BASE_DIR = Path(__file__).resolve().parent
        DB_PATH = BASE_DIR / "test_db.db"

        db_url = f"sqlite:///{DB_PATH}"
        connection = DataBaseConnection(db_url)
        connection.connect()