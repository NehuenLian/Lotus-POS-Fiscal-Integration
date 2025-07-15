import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
                               QLabel, QLineEdit, QPushButton, QStackedWidget,
                               QTableWidget, QVBoxLayout, QWidget)

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield)


class SalesViewManager(QWidget):
    def __init__(self, register_sale_controller):
        super().__init__()
        self.resize(1280, 720)

        self.components = UIComponents()
        self.main_window = QVBoxLayout(self)
        self.register_sale_controller = register_sale_controller

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

        header = display_header("Registrar venta")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget

    def _set_first_layout(self) -> QWidget:
        first_layout = QHBoxLayout()
        first_qwidget = QWidget()

        self.barcode_input_field = display_textfield(self._search_product_handler)

        send_button = display_send_button(self._search_product_handler)

        first_layout.addWidget(self.barcode_input_field)
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
    
    # Individual components
    def _display_table(self) -> QTableWidget:
        table = self.components.info_table()
        return table
    
    # Actions handlers
    def _search_product_handler(self):
        barcode = self.barcode_input_field.text()
        self.barcode_input_field.clear()
        self.register_sale_controller.remove_soon(barcode)


class UIComponents:
    def __init__(self):
        pass
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(9)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Cant. Disponible", "Precio", "Cantidad", "Subtotal", "Agregar", "Eliminar"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(1000)
        table.setFixedHeight(300)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table