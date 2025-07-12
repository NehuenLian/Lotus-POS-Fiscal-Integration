from src.data_access.connection import DataBaseConnection

db_url = "sqlite:///test_db.db"
connection = DataBaseConnection(db_url)  # Connection Singleton
connection.connect()  # Connect to db
