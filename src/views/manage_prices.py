from asyncio import new_event_loop
import re
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
                               QLabel, QLineEdit, QMessageBox, QPushButton,
                               QStackedWidget, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QDoubleSpinBox)

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield,
                                         show_message_box_notification)


class PriceViewManager(QWidget):
    def __init__(self, manage_prices_controller):
        super().__init__()

        self.components = DomainComponents()
        self.main_layout = QVBoxLayout(self)
        self.manage_prices_controller = manage_prices_controller

        self.product_id = None

        self._set_main_layout()

    # Set layouts
    def _set_main_layout(self) -> None:

        header_layout = self._set_header()
        search_layout = self._set_search_layout()
        table_layout = self._set_table_layout()
        update_price_layout = self._set_update_price_section()

        self.main_layout.addWidget(header_layout)
        self.main_layout.addWidget(search_layout)
        self.main_layout.addWidget(table_layout)
        self.main_layout.addWidget(update_price_layout)
        self.main_layout.addStretch(1)

    def _set_header(self) -> QWidget:
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = display_header("Gestionar Precios")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget

    def _set_search_layout(self) -> QWidget:
        search_layout = QHBoxLayout()
        search_qwidget = QWidget()

        self.barcode_input_field = display_textfield(self._search_product_handler)

        send_button = display_send_button(self._search_product_handler)

        search_layout.addWidget(self.barcode_input_field)
        search_layout.addWidget(send_button)
        search_layout.addStretch(1)

        search_qwidget.setLayout(search_layout)

        return search_qwidget
    
    def _set_table_layout(self) -> QWidget:

        table_layout = QVBoxLayout()
        table_qwidget = QWidget()

        self.table = self._display_table()
        divider = self._display_divider()

        table_layout.addWidget(self.table, alignment=Qt.AlignHCenter)
        table_layout.addSpacing(15)
        table_layout.addWidget(divider)
        table_layout.addStretch(1)
        table_qwidget.setLayout(table_layout)

        return table_qwidget
    
    def _set_update_price_section(self) -> QWidget:
        
        update_price_layout = QHBoxLayout()
        update_price_qwidget = QWidget()

        new_price_label, self.new_price_field, update_price_button = self._display_update_price_form()

        update_price_layout.addStretch(1)
        update_price_layout.addWidget(new_price_label)
        update_price_layout.addWidget(self.new_price_field)
        update_price_layout.addWidget(update_price_button)
        update_price_layout.addStretch(1)
        update_price_qwidget.setLayout(update_price_layout)

        return update_price_qwidget
    
    # Individual components
    def _display_table(self) -> QTableWidget:
        table = self.components.info_table()
        return table
    
    def _display_divider(self) -> QFrame:
        divider = self.components.horizontal_divider()
        return divider
    
    def _display_update_price_form(self) -> tuple[QLabel, QDoubleSpinBox, QPushButton]:
        new_price_label = self.components.input_new_price_label()
        new_price_field = self.components.new_price_field()
        update_price_button = self.components.update_price()

        update_price_button.clicked.connect(self._update_price_handler)

        return new_price_label, new_price_field, update_price_button
    
    # Actions handlers
    def _search_product_handler(self) -> None:
        barcode = self.barcode_input_field.text()
        self.barcode_input_field.clear()
        self.product_id = self.manage_prices_controller.get_product(barcode)

    # Update and manipulate view
    def display_product(self, product_id: int, product_barcode: Optional[str], product_name: str, product_price: Optional[int]) -> None:
        self.table.setRowCount(0)
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(str(product_id)))
        self.table.setItem(0, 1, QTableWidgetItem(product_barcode or ""))
        self.table.setItem(0, 2, QTableWidgetItem(product_name))
        self.table.setItem(0, 3, QTableWidgetItem(str(product_price) if product_price is not None else "0"))

    def _update_price_handler(self) -> None:
        new_price = self.new_price_field.text()
        choice = self.components.confirm_process_message_box()

        try:
            new_price_formatted = self._format_new_price_input(new_price)
        except ValueError:
            show_message_box_notification("Ingrese un precio válido.")
            return

        if self.product_id is None:
            show_message_box_notification("No se seleccionó ningún producto.")
            self._clear_view()
            return

        if new_price_formatted < 1:
            show_message_box_notification("El nuevo precio no puede ser negativo o menor a $1.")
            return

        if not choice:
            show_message_box_notification("El cambio de precio fue cancelado.")
            return

        self.manage_prices_controller.update_price(self.product_id, new_price_formatted)
        self._clear_view()

    # Auxiliar
    def _format_new_price_input(self, new_price) -> float:
        new_price_formatted = new_price.replace("$", "")
        return float(new_price_formatted)

    def _clear_view(self) -> None:
        self.table.setRowCount(0)
        self.new_price_field.clear()

    def show_notification_from_controller(self, message: str) -> None:
        show_message_box_notification(message)

class DomainComponents:
    def __init__(self):
        pass
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Precio"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(500)
        table.setFixedHeight(200)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table
    
    def horizontal_divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        return line
    
    def input_new_price_label(self) -> QLabel:
        new_price_label = QLabel("Nuevo precio (Formato ideal: $0.000.00 o $00.000.00): ")
        return new_price_label
    
    def new_price_field(self) -> QDoubleSpinBox:
        new_price_field = QDoubleSpinBox()
        new_price_field.setPrefix("$")
        new_price_field.setDecimals(2)
        new_price_field.setSingleStep(0.01)
        new_price_field.setMinimum(0.00)
        new_price_field.setMaximum(999999999.99)

        new_price_field.setFixedWidth(200)
        new_price_field.setFixedHeight(30)

        return new_price_field
    
    def update_price(self) -> QPushButton:
        update_button = QPushButton("Actualizar")
        return update_button
    
    def confirm_process_message_box(self) -> bool:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirmar cambio de precio")
        msg_box.setText("¿Confirmar?")
        msg_box.setIcon(QMessageBox.Question)

        confirm = msg_box.addButton("Confirmar", QMessageBox.AcceptRole)
        cancel = msg_box.addButton("Cancelar", QMessageBox.RejectRole)

        msg_box.exec()

        if msg_box.clickedButton() == confirm:
            return True
        else:
            return False
        