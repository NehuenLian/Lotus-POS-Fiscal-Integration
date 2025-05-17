from src.views.settings_view import SettingsViewManager
from src.database.connection import DataBaseConnection
from src.utils.logging_config import controller_logger
from decouple import config
from src.views.notifications import SnackBarNotifications
import os


class SettingsController:
    def __init__(self, page, cont):
        self.view = SettingsViewManager(page, cont, self)
        self.notification = SnackBarNotifications(page)

    def update_db_url(self, new_url):
        with open('.env', 'w') as f:
            f.write(f"DATABASE_URL={new_url}\n")
        try:
            os.environ["DATABASE_URL"] = new_url

            DataBaseConnection._instance = None
            connection = DataBaseConnection(new_url)
            connection.db_url = new_url

            controller_logger.info("Database Updated.")
            self.notification.snack_bar_neutral_message("Base de datos actualizada.")

        except:
            self.notification.snack_bar_error_message("URL Inválida, inténtelo de nuevo")

    def disconnect(self, e):
        if self.flag.connection_exists:
            db_url = config("DATABASE_URL")
            connection = DataBaseConnection(db_url)
            connection.close()
            self.notification.snack_bar_success_message("Desconexión exitosa.")
        else:
            self.notification.snack_bar_error_message("No hay una conexión activa.")
    