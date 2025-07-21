from src.business_logic.settings import SettingsManagement

class SettingsController:
    def __init__(self):
        self.settings_management = SettingsManagement()
        self._view = None

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view) -> None:
        self._view = view

    def connect_to_db(self, db_url: str) -> None:
        self.settings_management.connect_to_db(db_url)