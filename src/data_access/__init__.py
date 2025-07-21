from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 
DB_PATH = BASE_DIR / "test_db.db"

db_url = f"sqlite:///{DB_PATH}"
from src.data_access.connection import DataBaseConnection

connection = DataBaseConnection(db_url)
connection.connect()
