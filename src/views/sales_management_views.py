import flet as ft
import re
from src.exceptions import ProductNotFoundError

class SalesViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, sales_controller):
        self.page, self.cont = page, cont
        self.sales_controller = sales_controller

        self.title = None
        self.divider = None
        self.barcode_textfield = None
        self.search_button = None
        self.data_table = None
        self.data_table_row = None

        self.sale_total_dict = {}

        self.sale_total_label = None
        self.sale_total = 0

        self.pay_method_row = None
        self.pay_method_label = None

        self.show_all_elements()
        self.display_product()

        self.id_idx = {}

    def snack_bar_error_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message, 
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.RED))
    
    def snack_bar_success_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message,
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.GREEN))
    
    def show_all_elements(self):
        self.title = ft.Row([ft.Text("Ventas", 
                                    size=30, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER)
        
        self.divider = ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)
        self.barcode_textfield = ft.TextField(label="Ingrese el código del producto...", width=300 ,on_submit=self.search_product_handler)

        self.search_button = ft.ElevatedButton("Obtener", 
                                            on_click=self.search_product_handler,
                                            bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        
        self.sale_total_label = ft.Text(f"Total: $0.  ", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.pay_method_label = ft.Text(f"Método de pago: Ninguno", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

        cash_button = ft.ElevatedButton("Efectivo", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=lambda e: self.set_pay_method(cash_button.text))
        transfer_button = ft.ElevatedButton("Transferencia", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=lambda e: self.set_pay_method(transfer_button.text))

        self.register_sale_button = ft.ElevatedButton("Completar venta", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.register_sale)

        self.pay_method_row = ft.Row([cash_button, transfer_button], ft.MainAxisAlignment.CENTER)

        self.input_and_button_row = ft.Row([self.barcode_textfield, self.search_button, self.sale_total_label, self.pay_method_label, self.register_sale_button], alignment=ft.MainAxisAlignment.START)

        self.cont.controls = [self.title, self.divider, self.input_and_button_row]
        self.page.update()

    def display_product(self):

        self.data_table = ft.DataTable(
            bgcolor=ft.Colors.BLUE_GREY_900,
            border=ft.border.all(2, ft.Colors.BLUE_GREY_500),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="ID", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Código", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Nombre del Producto", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Cantidad Disponible", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Precio", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Cantidad", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Subtotal", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Agregar", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Eliminar", color=ft.Colors.WHITE)),
                ],
            rows = []
            )
        self.cont.controls = [self.title, self.divider, self.input_and_button_row, self.data_table, self.pay_method_row, self.register_sale_button]
        self.page.update()

    def show_product_in_table(self, barcode):

        id = self.sales_controller.get_id(barcode)
        product = self.sales_controller.get_product(id)
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

        self.data_table.rows.append(new_row)
        self.build_id_idx_dict()

        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)
        self.sale_total_label.value = f"Total: ${self.sale_total}"
        self.cont.controls = [self.title, self.divider, self.input_and_button_row, self.data_table_row, self.pay_method_row, self.register_sale_button]
        self.page.update()

    def update_row(self, product_id):

        product = self.sale_total_dict[product_id]

        if product_id in self.id_idx:
            row_index = self.id_idx[product_id]

        self.data_table.rows[row_index].cells[5].content = ft.Text(value=str(product['quantity']))
        self.data_table.rows[row_index].cells[6].content = ft.Text(value=f"${product['subtotal']}")

        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)
        self.sale_total_label.value = f"Total: ${self.sale_total}"
        self.cont.controls = [self.title, self.divider, self.input_and_button_row, self.data_table_row, self.pay_method_row, self.register_sale_button]
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

            self.snack_bar_error_message("No quedan existencias para seguir agregando productos.")
            
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
                    self.data_table.rows.pop(row_index)
                    self.build_id_idx_dict()
                    self.page.update()

    def set_pay_method(self, method):
        self.pay_method_label.value = f"Método de pago: {method}"
        self.page.update()

        self.sales_controller.choose_pay_method(method)

    def register_sale(self, e):
        if not self.sale_total_dict:
            self.snack_bar_error_message("Por favor, seleccione al menos un producto.")
        elif self.pay_method_label.value == "Método de pago: Ninguno":
            self.snack_bar_error_message("Por favor, seleccione un método de pago.")
        else:
            self.sales_controller.complete_sale()
            self.snack_bar_success_message("Venta registrada exitosamente.")
            self.reset_page_default()
            print(self.sale_total_dict)

    # Handlers
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):
            try:
                self.show_product_in_table(barcode)
            except ProductNotFoundError:
                self.snack_bar_error_message("Producto no encontrado.")
        else:
            self.snack_bar_error_message("No se permiten caracteres especiales.")

    #Aux
    def reset_page_default(self):
        self.data_table.rows.clear()
        self.sale_total_dict = {}
        self.sale_total_label.value = "Total: $0.  "
        self.pay_method_label.value = f"Método de pago: Ninguno"
        self.page.update()

    def build_id_idx_dict(self):
        for index, row in enumerate(self.data_table.rows):
            row_content = row.cells[0].content.value
            row_index = index

            self.id_idx[row_content] = row_index