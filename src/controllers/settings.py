

class SettingsController:
    def __init__(self):

        self._view = None

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view) -> None:
        self._view = view

    def connect_to_db(self) -> None:
        print("Estableciendo conexion...")