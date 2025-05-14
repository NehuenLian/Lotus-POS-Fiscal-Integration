from src.views.settings_view import SettingsViewManager
from src.database.connection import DataBaseConnection
from src.database.models import initialize_database
from src.utils.logging_config import controller_logger

from decouple import config


class SettingsController:
    def __init__(self, page, cont):
        self.view = SettingsViewManager(page, cont, self)

    def update_db_url(self, new_url):
        with open('.env', 'w') as f:
            f.write(f"DATABASE_URL={new_url}\n")

        controller_logger.info("Database Updated.")

    def connect_to_new_db(self, e):
        db_url = config("DATABASE_URL")
        connection = DataBaseConnection(db_url)
        connection.connect()
        controller_logger.info("Connection to new database succesfully.")
        initialize_database(connection)
        controller_logger.info("Tables mapped successfully. The mapping process was completed without errors, and all tables were correctly assigned.")