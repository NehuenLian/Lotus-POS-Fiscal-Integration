import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
                               QLabel, QLineEdit, QPushButton, QStackedWidget,
                               QTableView, QTableWidget, QVBoxLayout, QWidget)


class CheckStockViewManager(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.components = UIComponents()
        self.main_window = QVBoxLayout(self)

        self._set_main_layout()

    # Set layouts
    def _set_main_layout(self):

        header_layout = self._set_header()
        first_layout = self._set_first_layout()
        second_layout = self._set_second_layout()

        self.main_window.addWidget(header_layout)
        self.main_window.addWidget(first_layout)
        self.main_window.addWidget(second_layout)

    def _set_header(self):
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = self._display_header()

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget

    def _set_first_layout(self) -> QWidget:

        first_layout = QHBoxLayout()
        first_qwidget = QWidget()

        barcode_input_field = self._display_textfield()
        send_button = self._display_send_button()

        first_layout.addWidget(barcode_input_field)
        first_layout.addWidget(send_button)
        first_layout.addStretch(1)

        first_qwidget.setLayout(first_layout)

        return first_qwidget
    
    def _set_second_layout(self) -> QWidget:

        second_layout = QVBoxLayout()
        second_qwidget = QWidget()

        table = self._display_table()

        second_layout.addWidget(table, alignment=Qt.AlignHCenter)
        second_layout.addStretch(1)
        second_qwidget.setLayout(second_layout)

        return second_qwidget
    
    # Individual components handler
    def _display_header(self) -> QLabel:
        header_label = self.components.header()
        return header_label

    def _display_textfield(self) -> QLineEdit:
        input_field = self.components.input_barcode()
        return input_field
    
    def _display_send_button(self) -> QPushButton:
        button = self.components.send_button()
        return button
    
    def _display_table(self) -> QTableWidget:
        table = self.components.info_table()
        return table
    
    # Ignore
    def request_barcode(self):
        pass

    def display_product(self):
        pass


class UIComponents:
    def __init__(self):
        pass

    def header(self):
        header_label = QLabel("Consultar Stock")
        return header_label

    def input_barcode(self) -> QLineEdit:
        input_field = QLineEdit()

        input_field.setPlaceholderText("Ingrese el código de barras...")

        input_field.setFixedWidth(200)
        input_field.setFixedHeight(30)

        input_field.setMaxLength(40)

        return input_field

    def send_button(self) -> QPushButton:
        button = QPushButton("Enviar")
        button.setFixedWidth(100)
        button.setFixedHeight(30)

        return button
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Stock"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(500)
        table.setFixedHeight(200)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table