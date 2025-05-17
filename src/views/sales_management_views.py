import flet as ft
import re
from src.exceptions import ProductNotFoundError
from src.utils.flags import FlagManager
from src.views.notifications import SnackBarNotifications


class SalesViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, sales_controller):
        self.page, self.cont = page, cont
        self.sales_controller = sales_controller
        self.notification = SnackBarNotifications(page)
        self.components = UIComponents(self)
        self.flags = FlagManager()

        self.barcode_textfield = ft.Ref[ft.TextField]()

        self.data_table = ft.Ref[ft.DataTable]()
        self.data_table_row = None

        self.sale_total_label = ft.Ref[ft.Text]()
        self.sale_total = 0

        self.pay_method_label = ft.Ref[ft.Text]()

        self._build_layout()

        self.sale_total_dict = {}
        self.id_idx = {}
    
    def _build_layout(self):
        header = self.components.show_header()
        search = self.components.show_search_controls()
        table = self.components.show_products_table()

        bottom_labels = self.components.show_bottom_labels()
        bottom_divider = self.components.set_divider()
        pay_methods = self.components.pay_methods_buttons()

        self.cont.controls = [
                            header,
                            search,
                            table,
                            bottom_divider,
                            bottom_labels,
                            pay_methods
                        ]

        self.page.update()

    def show_product_in_table(self, product):

        product_id = product.product_id

        if product_id in self.sale_total_dict:

            products = self.sale_total_dict.get(product_id)

            products['quantity'] += 1
            products['subtotal'] = products['customer_price'] * products['quantity']
            self.sale_total += self.sale_total_dict[product_id]['customer_price']
            self.update_row(product_id)

        else:
            self.sale_total_dict[product_id] = {
                "product_barcode": product.barcode,
                "product_name": product.product_name,
                "available_quantity": product.available_quantity,
                "customer_price": product.customer_price,
                "quantity" : 1,
                "subtotal" : product.customer_price,
                }
            
            self.sale_total += self.sale_total_dict[product_id]['customer_price']
            self.add_row()

    def add_row(self):
        for product_id, product_info in self.sale_total_dict.items():

            new_row = ft.DataRow(data=product_id,
                cells=[
                    ft.DataCell(ft.Text(product_id)),
                    ft.DataCell(ft.Text(product_info['product_barcode'])),
                    ft.DataCell(ft.Text(product_info['product_name'])),
                    ft.DataCell(ft.Text(product_info['available_quantity'])),
                    ft.DataCell(ft.Text(f"${product_info['customer_price']}")),
                    ft.DataCell(ft.Text(product_info['quantity'])),
                    ft.DataCell(ft.Text(f"${product_info['subtotal']}")),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.ADD,icon_color=ft.Colors.GREEN_400, on_click=lambda e: self.add_product(product_id))),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE,icon_color=ft.Colors.RED_400, on_click=lambda e: self.delete_product(product_id))),
                ]
            )

        self.data_table.current.rows.append(new_row)
        self.build_id_idx_dict()

        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)
        self.sale_total_label.current.value = f"Total: ${self.sale_total}"
        self.data_table.current.update()
        self.page.update()

    def update_row(self, product_id):

        product = self.sale_total_dict[product_id]

        if product_id in self.id_idx:
            row_index = self.id_idx[product_id]

        self.data_table.current.rows[row_index].cells[5].content = ft.Text(value=str(product['quantity']))
        self.data_table.current.rows[row_index].cells[6].content = ft.Text(value=f"${product['subtotal']}")

        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)
        self.sale_total_label.current.value = f"Total: ${self.sale_total}"

        self.data_table.current.update()
        self.page.update()

    def add_product(self, id_to_add):

        products = self.sale_total_dict.get(id_to_add)

        barcode = products['product_barcode']
        product_name = products['product_name']
        available_quantity = products['available_quantity']
        customer_price = products['customer_price']

        self.sales_controller.add_new_product(id_to_add, barcode, product_name, available_quantity, customer_price)

        if products['quantity'] < products['available_quantity']:
            products['quantity'] += 1
            products['subtotal'] += products['customer_price']
            self.sale_total += products['customer_price']
            self.update_row(id_to_add)

        elif products['quantity'] >= products['available_quantity']:

            self.notification.snack_bar_error_message("No quedan existencias para seguir agregando productos.")
            
    def delete_product(self, id_to_cancel):
            self.sales_controller.remove_product(id_to_cancel)
            products = self.sale_total_dict.get(id_to_cancel)

            if products['quantity'] > 1:
                products['quantity'] -= 1
                products['subtotal'] -= products['customer_price']
                self.sale_total -= products['customer_price']
                self.update_row(id_to_cancel)

            elif products['quantity'] == 1:
                del self.sale_total_dict[id_to_cancel]

                if id_to_cancel in self.id_idx:
                    row_index = self.id_idx[id_to_cancel]
                    self.data_table.current.rows.pop(row_index)
                    self.build_id_idx_dict()
                    self.data_table.current.update()
                    
                    self.sale_total -= products['customer_price']
                    self.sale_total_label.current.value = f"Total: ${self.sale_total}"

                    self.page.update()

    def set_pay_method(self, method):
        self.pay_method_label.current.value = f"Método de pago: {method}"
        self.page.update()

        self.sales_controller.choose_pay_method(method)

    def register_sale(self, e):
        if not self.sale_total_dict:
            self.notification.snack_bar_error_message("Por favor, seleccione al menos un producto.")
        elif self.pay_method_label.current.value == "Método de pago: Ninguno":
            self.notification.snack_bar_error_message("Por favor, seleccione un método de pago.")
        else:
            self.sales_controller.complete_sale()
            self.notification.snack_bar_success_message("Venta registrada exitosamente.")
            self.reset_page_default()

    # Handler
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.current.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):

            if self.flags.connection_exists:
                try:
                    id = self.sales_controller.get_id(barcode)
                    product = self.sales_controller.get_product(id)
                    self.show_product_in_table(product)
                    
                except ProductNotFoundError:
                    self.notification.snack_bar_error_message("Producto no encontrado.")

            else:
                self.notification.snack_bar_error_message("No se detectó una conexión a una base de datos.")

        else:
            self.notification.snack_bar_error_message("No se permiten caracteres especiales.")

    # Aux
    def reset_page_default(self):
        self.data_table.current.rows.clear()
        self.sale_total_dict = {}
        self.sale_total_label.current.value = "Total: $0.  "
        self.pay_method_label.current.value = f"Método de pago: Ninguno"
        self.page.update()

    def build_id_idx_dict(self):
        for index, row in enumerate(self.data_table.current.rows):
            row_content = row.cells[0].content.value
            row_index = index

            self.id_idx[row_content] = row_index

class UIComponents:
    def __init__(self, sales_view_manager):
        self.sales_view_manager = sales_view_manager

    def show_header(self):
        title = ft.Text("Ventas", size=15, weight=ft.FontWeight.BOLD)
        top_divider = ft.Divider(height=1)

        return ft.Column([title, top_divider])
    
    def show_search_controls(self):
        barcode_field =  ft.TextField(ref=self.sales_view_manager.barcode_textfield ,label="Ingrese el código del producto...", width=300 ,on_submit=self.sales_view_manager.search_product_handler)
        obtain_product_button = ft.ElevatedButton("Obtener", on_click=self.sales_view_manager.search_product_handler)
        register_sale_button = ft.ElevatedButton("Completar venta", on_click=self.sales_view_manager.register_sale)
    
        return ft.Row([ft.Row([barcode_field, obtain_product_button], spacing=10), register_sale_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def show_products_table(self):

        table = ft.DataTable(ref=self.sales_view_manager.data_table,
        border=ft.border.all(2, ft.Colors.BLUE_GREY_200),
        vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="ID")),
                ft.DataColumn(ft.Text(value="Código")),
                ft.DataColumn(ft.Text(value="Nombre del Producto")),
                ft.DataColumn(ft.Text(value="Cantidad Disponible")),
                ft.DataColumn(ft.Text(value="Precio")),
                ft.DataColumn(ft.Text(value="Cantidad")),
                ft.DataColumn(ft.Text(value="Subtotal")),
                ft.DataColumn(ft.Text(value="Agregar")),
                ft.DataColumn(ft.Text(value="Eliminar")),
                ],
            rows = []
            )
        
        return ft.Container(content=ft.Column([ft.Row([table], alignment=ft.MainAxisAlignment.CENTER)], scroll="auto"), expand=True)
    
    def set_divider(self):
        return ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)

    def show_bottom_labels(self):
        pay_method_label = ft.Text(f"Método de pago: Ninguno", ref=self.sales_view_manager.pay_method_label, size=22)
        sale_total_label = ft.Text(f"Total: $0.  ", ref=self.sales_view_manager.sale_total_label, size=22)

        return ft.Column([ft.Row([pay_method_label, sale_total_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)])

    def pay_methods_buttons(self):
        cash_button = ft.ElevatedButton("Efectivo", on_click=lambda e: self.sales_view_manager.set_pay_method(cash_button.text))
        transfer_button = ft.ElevatedButton("Transferencia", on_click=lambda e: self.sales_view_manager.set_pay_method(transfer_button.text))
        
        return ft.Row([cash_button, transfer_button])