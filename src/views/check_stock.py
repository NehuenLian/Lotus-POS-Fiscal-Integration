import re
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QHBoxLayout, QStackedWidget, QFrame
)

class CheckStockViewManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lotus POS")
        self.resize(1280, 720)
        print("Hola estas en CheckStockViewManager")

    def request_barcode(self):
        pass

    def display_product(self):
        pass
