import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
                               QLabel, QLineEdit, QPushButton, QStackedWidget,
                               QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem)

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield)


class SalesViewManager(QWidget):
    def __init__(self, register_sale_controller):
        super().__init__()
        self.resize(1280, 720)

        self.components = DomainComponents()
        self.main_window = QVBoxLayout(self)
        self.register_sale_controller = register_sale_controller

        self.products = {}
        self.id_idx = {}

        self._set_main_layout()
        
    # Set layouts
    def _set_main_layout(self) -> None:

        header_layout = self._set_header()
        first_layout = self._set_first_layout()
        second_layout = self._set_second_layout()

        self.main_window.addWidget(header_layout)
        self.main_window.addWidget(first_layout)
        self.main_window.addWidget(second_layout)

    def _set_header(self) -> QWidget:
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
        self.register_sale_controller.get_product(barcode)

    def _add_new_product(self) -> None:

        new_row = self.table.rowCount()
        self.table.insertRow(new_row)

        last_id, last_product = next(reversed(self.products.items()))
        
        price = last_product["customer_price"]
        quantity = last_product["quantity"]
        subtotal = price * quantity

        self.table.setItem(new_row, 0, QTableWidgetItem(str(last_id)))
        self.table.setItem(new_row, 1, QTableWidgetItem(str(last_product["product_barcode"])))
        self.table.setItem(new_row, 2, QTableWidgetItem(str(last_product["product_name"])))
        # self.table.setItem(new_row, 3, QTableWidgetItem(str(last_product["available_quantity"])))
        self.table.setItem(new_row, 3, QTableWidgetItem(str(last_product["customer_price"])))
        self.table.setItem(new_row, 4, QTableWidgetItem(str(quantity)))
        self.table.setItem(new_row, 5, QTableWidgetItem(str(subtotal)))

        btn_add = QPushButton("+")
        btn_add.clicked.connect(lambda _, p_id=last_id: self._add_one(p_id))
        self.table.setCellWidget(new_row, 6, btn_add)

        btn_del = QPushButton("-")
        btn_del.clicked.connect(lambda _, p_id=last_id: self._delete_one(p_id))
        self.table.setCellWidget(new_row, 7, btn_del)

        self._build_id_idx_dict()

    def _update_row(self, p_id: int) -> None:
        product_info = self.products[p_id]

        if p_id in self.id_idx:
            row_index = self.id_idx[p_id]

            self.table.setItem(row_index, 4, QTableWidgetItem(str(product_info["quantity"])))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(product_info["subtotal"])))

    def _add_one(self, p_id: int) -> None:
        
        self.register_sale_controller.add_new_product(
            p_id,
            self.products[p_id]["product_barcode"],
            self.products[p_id]["product_name"],
            self.products[p_id]["available_quantity"],
            self.products[p_id]["customer_price"],
        )

        self.products[p_id]["quantity"] += 1
        self.products[p_id]["subtotal"] += self.products[p_id]["customer_price"]

        self._update_row(p_id)

    def _delete_one(self, p_id) -> None:

        if self.products[p_id]["quantity"] > 1:
            self.products[p_id]["quantity"] -= 1
            self.products[p_id]["subtotal"] -= self.products[p_id]["customer_price"]
            self._update_row(p_id)
            
        else:
            self.products.pop(p_id)
            self.table.removeRow(self.id_idx[p_id])
            self._build_id_idx_dict()

    # Auxiliar
    def create_view_product(self, product) -> None:

        for product_id, product_info in self.products.items():
            if product_id == product.product_id:
                product_info["quantity"] += 1
                product_info["subtotal"] += product_info["customer_price"]
                self._update_row(product.product_id)
                return

        productid = product.product_id
        self.products[int(productid)] = {
                "product_barcode": product.barcode,
                "product_name": product.product_name,
                "available_quantity": product.available_quantity,
                "customer_price": product.customer_price,
                "quantity" : 1,
                "subtotal" : product.customer_price,
                }
        self._add_new_product()

    def _build_id_idx_dict(self) -> None:
        self.id_idx.clear()
        row_count = self.table.rowCount()

        for row in range(row_count):
            item = self.table.item(row, 0)
            if item:
                product_id = int(item.text())
                self.id_idx[product_id] = row


class DomainComponents:
    def __init__(self):
        pass
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Precio", "Cantidad", "Subtotal", "Agregar", "Eliminar"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(1000)
        table.setFixedHeight(300)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table