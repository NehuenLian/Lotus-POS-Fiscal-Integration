from pathlib import Path

# Ruta absoluta al archivo test_db.db dentro de data_access/
BASE_DIR = Path(__file__).resolve().parent  # Esto apunta a /src/data_access/
DB_PATH = BASE_DIR / "test_db.db"

db_url = f"sqlite:///{DB_PATH}"
from src.data_access.connection import DataBaseConnection

connection = DataBaseConnection(db_url)
connection.connect()
