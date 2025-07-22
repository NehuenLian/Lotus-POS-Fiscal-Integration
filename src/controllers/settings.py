import os
import sys

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

    def update_db_url(self, db_url: str) -> None:
        self.settings_management.update_db_url(db_url)

    def restart_program(self) -> None:
        """Close and relaunch app"""
        python = sys.executable
        os.execl(python, python, *sys.argv)