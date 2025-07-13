import re
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QHBoxLayout, QStackedWidget, QFrame
)


class PriceViewsManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lotus POS")
        self.resize(1280, 720)
        print("Hola estas en PriceViewsManager")
