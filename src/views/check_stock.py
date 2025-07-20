import re
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield,
                                         show_message_box_notification)


class CheckStockViewManager(QWidget):
    def __init__(self, check_stock_controller):
        super().__init__()

        self.components = DomainComponents()
        self.main_window = QVBoxLayout(self)
        self.check_stock_controller = check_stock_controller

        self._set_main_layout()


    # Set layouts
    def _set_main_layout(self) -> None:

        header_layout = self._set_header()
        first_layout = self._set_search_layout()
        second_layout = self._set_table_layout()

        self.main_window.addWidget(header_layout)
        self.main_window.addWidget(first_layout)
        self.main_window.addWidget(second_layout)

    def _set_header(self) -> QWidget:
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = display_header("Consultar Stock")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget

    def _set_search_layout(self) -> QWidget:
        first_layout = QHBoxLayout()
        first_qwidget = QWidget()

        self.barcode_input_field = display_textfield(self._search_product_handler)

        send_button = display_send_button(self._search_product_handler)

        first_layout.addWidget(self.barcode_input_field)
        first_layout.addWidget(send_button)
        first_layout.addStretch(1)

        first_qwidget.setLayout(first_layout)

        return first_qwidget
    
    def _set_table_layout(self) -> QWidget:

        second_layout = QVBoxLayout()
        second_qwidget = QWidget()

        self.table = self._display_table()

        second_layout.addWidget(self.table, alignment=Qt.AlignHCenter)
        second_layout.addStretch(1)
        second_qwidget.setLayout(second_layout)

        return second_qwidget


    # Individual components
    def _display_table(self) -> QTableWidget:
        table = self.components.info_table()
        return table


    # Actions handlers
    def _search_product_handler(self) -> None:
        
        barcode = self.barcode_input_field.text()
        self.barcode_input_field.clear()
        self.check_stock_controller.get_product(barcode)


    # Update and manipulate view
    def display_product(self,product_id: int,product_barcode: Optional[str],product_name: str,available_quantity: Optional[int]) -> None:
        self.table.setRowCount(0)
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(str(product_id)))
        self.table.setItem(0, 1, QTableWidgetItem(product_barcode or ""))
        self.table.setItem(0, 2, QTableWidgetItem(product_name))
        self.table.setItem(0, 3, QTableWidgetItem(str(available_quantity) if available_quantity is not None else "0"))


    # Auxiliar
    def show_notification_from_controller(self, message: str) -> None:
        show_message_box_notification(message)


class DomainComponents:
    def __init__(self):
        pass
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Stock"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(500)
        table.setFixedHeight(200)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table