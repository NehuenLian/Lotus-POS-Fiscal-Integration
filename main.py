from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController

def load_stylesheet(app):
    with open("src/views/assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("src/views/assets/app_icon.ico")) # App Icon
    load_stylesheet(app)
    controller = MainController()
    controller.ui.show()
    app.exec()