from PySide6.QtWidgets import QApplication
from src.controllers.main_controller import MainController

if __name__ == "__main__":
    app = QApplication([])
    controller = MainController()
    controller.ui.show()
    app.exec()