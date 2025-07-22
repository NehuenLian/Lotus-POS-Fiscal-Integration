from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield, horizontal_divider,
                                         show_message_box_notification)


class SalesViewManager(QWidget):
    def __init__(self, register_sale_controller):
        super().__init__()

        self.components = DomainComponents()
        self.main_layout = QVBoxLayout(self)
        self.register_sale_controller = register_sale_controller

        self.products = {}
        self.id_idx = {}

        # Global access values
        self.total_label = None # Qlabel
        self.pay_method_label = None # Qlabel
        self.is_pay_method_selected = False # Boolean

        # Display whole view
        self._set_main_layout()


    # Set layouts
    def _set_main_layout(self) -> None:

        header_layout = self._set_header()
        search_layout = self._set_search_and_total_layout()
        table_layout = self._set_table_layout()
        third_layout = self._set_payment_selection_layout()
        bottom_layout = self._register_sale_layout()

        self.main_layout.addWidget(header_layout)
        self.main_layout.addWidget(search_layout)
        self.main_layout.addWidget(table_layout)
        self.main_layout.addWidget(third_layout)
        self.main_layout.addWidget(bottom_layout)
        self.main_layout.addStretch(1)

    def _set_header(self) -> QWidget:
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = display_header("Registrar venta")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget

    def _set_search_and_total_layout(self) -> QWidget:
        search_layout = QHBoxLayout()
        search_qwidget = QWidget()

        self.barcode_input_field = display_textfield(self._search_product_handler)
        self.total_label = self._display_total_label()

        send_button = display_send_button(self._search_product_handler)

        search_layout.addWidget(self.barcode_input_field)
        search_layout.addWidget(send_button)
        search_layout.addStretch(1)
        search_layout.addWidget(self.total_label)

        search_qwidget.setLayout(search_layout)

        return search_qwidget
    
    def _set_table_layout(self) -> QWidget:

        table_layout = QVBoxLayout()
        table_qwidget = QWidget()

        self.table = self._display_table()
        divider = horizontal_divider()

        table_layout.addWidget(self.table, alignment=Qt.AlignHCenter)
        table_layout.addSpacing(15)
        table_layout.addWidget(divider)
        table_layout.addStretch(1)
        table_qwidget.setLayout(table_layout)

        return table_qwidget
    
    def _set_payment_selection_layout(self) -> QWidget:

        outer_layout = QVBoxLayout()
        outer_widget = QWidget()

        buttons_layout = QHBoxLayout()
        buttons_widget = QWidget()

        self.pay_method_label, cash_button, transfer_button, card_button = self._display_payment_selection_buttons()
        
        buttons_layout.addWidget(self.pay_method_label)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(cash_button)
        buttons_layout.addWidget(transfer_button)
        buttons_layout.addWidget(card_button)

        buttons_widget.setLayout(buttons_layout)

        outer_layout.addWidget(buttons_widget)
        outer_widget.setLayout(outer_layout)

        return outer_widget
    
    def _register_sale_layout(self) -> QWidget:

        bottom_layout = QVBoxLayout()
        bottom_qwidget = QWidget()

        divider, register_sale_button = self._display_register_sale_button()

        bottom_layout.addWidget(divider)
        bottom_layout.addSpacing(15)
        bottom_layout.addWidget(register_sale_button)
        bottom_qwidget.setLayout(bottom_layout)

        return bottom_qwidget


    # Individual components
    def _display_table(self) -> QTableWidget:
        table = self.components.info_table()
        return table
    
    def _display_total_label(self) -> QLabel:
        total_label = self.components.total_sale_label()
        return total_label
    
    def _display_payment_selection_buttons(self) -> Tuple[QLineEdit, QPushButton, QPushButton, QPushButton]:
        pay_method_label, cash_button, transfer_button, card_button = self.components.pay_method_section()
        
        cash_button.clicked.connect(lambda: self._set_pay_method_handler("Efectivo"))
        transfer_button.clicked.connect(lambda: self._set_pay_method_handler("Transferencia"))
        card_button.clicked.connect(lambda: self._set_pay_method_handler("Tarjeta"))

        return pay_method_label, cash_button, transfer_button, card_button
    
    def _display_register_sale_button(self) -> Tuple[QLabel, QPushButton]:

        divider = horizontal_divider()
        register_sale_button = self.components.register_sale_button()
        register_sale_button.clicked.connect(self._register_sale_handler)

        return divider, register_sale_button


    # Handlers
    def _search_product_handler(self) -> None:

        barcode = self.barcode_input_field.text()
        self.barcode_input_field.clear()
        self.register_sale_controller.get_product(barcode)

    def _set_pay_method_handler(self, pay_method: str) -> None:
        self.register_sale_controller.select_pay_method(pay_method)
        self._set_pay_method(pay_method)
        self.is_pay_method_selected = True

    def _register_sale_handler(self):

        if not self.products:
            show_message_box_notification("Seleccione al menos un producto.")
            return

        if not self.is_pay_method_selected:
            show_message_box_notification("Seleccione un método de pago.")
            return

        self.register_sale_controller.complete_sale()
        self._clear_view()


    # Logic actions
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

        self._calculate_total()

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
            self._calculate_total()

    def _set_pay_method(self, method) -> None:
        self.pay_method_label.setText(f"Método de pago: {method}")

    def _calculate_total(self) -> None:
        subtotals_list = []
        for product in self.products.values():
            subtotals_list.append(int(product["subtotal"]))

        current_total = sum(subtotals_list)
        self.total_label.setText(f"Total: ${current_total}")


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
        self._calculate_total()

    def _build_id_idx_dict(self) -> None:
        self.id_idx.clear()
        row_count = self.table.rowCount()

        for row in range(row_count):
            item = self.table.item(row, 0)
            if item:
                product_id = int(item.text())
                self.id_idx[product_id] = row

    def _clear_view(self) -> None:
        self.total_label.setText("Total: $0")
        self.pay_method_label.setText("Método de pago:  ")
        self.id_idx.clear()
        self.products.clear()
        self.table.setRowCount(0)

    def show_notification_from_controller(self, message: str) -> None:
        show_message_box_notification(message)

class DomainComponents:
    def __init__(self):
        pass
    
    def info_table(self) -> QTableWidget:
        table = QTableWidget()

        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Precio", "Cantidad", "Subtotal", "Agregar", "Eliminar"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setFixedWidth(1100)
        table.setFixedHeight(400)

        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        return table
    
    def pay_method_section(self) -> Tuple[QLabel, QPushButton, QPushButton, QPushButton]:

        pay_method_label = QLabel("Método de pago:  ")

        cash_button = QPushButton("Efectivo")
        cash_button.setFixedWidth(100)
        cash_button.setFixedHeight(30)

        transfer_button = QPushButton("Transferencia")
        transfer_button.setFixedWidth(100)
        transfer_button.setFixedHeight(30)

        card_button = QPushButton("Tarjeta")
        card_button.setFixedWidth(100)
        card_button.setFixedHeight(30)

        return pay_method_label, cash_button, transfer_button, card_button
    
    def total_sale_label(self) -> QLabel:
        total_label = QLabel("Total: $0")
        return total_label

    def register_sale_button(self) -> QPushButton:
        register_sale = QPushButton("REGISTRAR VENTA")
        return register_sale