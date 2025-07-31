from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController

def load_stylesheet(app):
    with open("src/views/assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication([])
    load_stylesheet(app)
    load_dotenv(override=True)
    controller = MainController()
    controller.ui.show()
    app.exec()