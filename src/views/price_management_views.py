import flet as ft
import re
from src.exceptions import ProductNotFoundError

class PriceViewsManager:
    def __init__(self, page: ft.Page, cont: ft.Column, prices_controller):
        self.page, self.cont = page, cont
        self.prices_controller = prices_controller

        self.title = None
        self.divider = None
        self.barcode_textfield = None
        self.search_button = None
        self.data_table = None
        self.data_table_row = None
        self.update_price_row = None
        self.confirm_question_row = None

        self.current_price_label = None
        self.new_price = None

        self.confirm_label = None
        self.no_button = None
        self.yes_button = None

        self.product_id = None
        self.new_price_textfield = None
        self.change_price_button = None

        self.error_message = None
        self.success_message = None

        self.input_and_button_row = None

        self.request_barcode()

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

    def request_barcode(self):
        self.title = ft.Row([ft.Text("Gestionar Precios", 
                                    size=30, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER)
        
        self.divider = ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)
        self.barcode_textfield = ft.TextField(label="Ingrese el código del producto...", width=300 ,on_submit=self.search_product_handler)
        self.search_button = ft.ElevatedButton("Obtener", 
                                            on_click=self.search_product_handler,
                                            bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        self.input_and_button_row = ft.Row([self.barcode_textfield, self.search_button], alignment=ft.MainAxisAlignment.CENTER)

        self.cont.controls = [self.title, self.divider, self.input_and_button_row]
        self.page.update()

    def display_product(self, id, product_name, current_price):

        self.data_table = ft.DataTable(
            bgcolor=ft.Colors.BLUE_GREY_900,
            border=ft.border.all(2, ft.Colors.BLUE_GREY_500),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="ID", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Nombre del Producto", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Precio actual", color=ft.Colors.WHITE)),
            ])

        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(id)), 
                ft.DataCell(ft.Text(product_name)),
                ft.DataCell(ft.Text(f"${current_price}"))
                ])
        
        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)

        self.data_table.rows.append(new_row)
        self.cont.controls = [self.title, self.divider, self.input_and_button_row, self.data_table_row]
        self.page.update()

    def set_new_price(self, current_price) -> float:
        self.current_price_label = ft.Text(value=f"Precio actual: ${current_price}")
        self.new_price_textfield = ft.TextField(label="$ ", input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(\.\d*)?$"))
        self.change_price_button = ft.ElevatedButton("Actualizar", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.confirm_changes_qt)

        self.update_price_row = ft.Row([self.current_price_label, self.new_price_textfield, self.change_price_button], alignment=ft.MainAxisAlignment.CENTER)

        self.cont.controls = [self.title,
                            self.divider,
                            self.input_and_button_row, 
                            self.data_table_row, 
                            self.update_price_row]
        
        self.page.update()

    def confirm_changes_qt(self, e):
        self.confirm_label = ft.Text("Confirmar cambios", weight=ft.FontWeight.BOLD)
        self.no_button = ft.ElevatedButton("Aceptar",
                                           on_click=self.update_price_handler,
                                            bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        
        self.yes_button = ft.ElevatedButton("Cancelar", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.cancel_operation)

        self.confirm_question_row = ft.Row([self.confirm_label, self.no_button, self.yes_button], alignment=ft.MainAxisAlignment.CENTER)

        self.cont.controls = [self.title,
                            self.divider,
                            self.input_and_button_row, 
                            self.data_table_row, 
                            self.update_price_row,
                            self.confirm_question_row]

        self.page.update()

    # Handlers
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):
            try:
                id, product_name, current_price = self.prices_controller.check_product(barcode)
                self.product_id = id
                self.display_product(id, product_name, current_price)
                self.set_new_price(current_price)
            except ProductNotFoundError:
                self.snack_bar_error_message("Producto no encontrado.")
        else:
            self.snack_bar_error_message("No se permiten caracteres especiales.")

    def update_price_handler(self, e):
        self.new_price = float(self.new_price_textfield.value)
        if self.new_price > 0:
            self.prices_controller.update_price(self.product_id, self.new_price_textfield.value)
            self.snack_bar_success_message("Precio actualizado correctamente.")
            self.reset_page_default()
        elif self.new_price <= 0:
            self.snack_bar_error_message("No se puede ingresar un precio menor a $0.")

    # Aux
    def cancel_operation(self, e):
        self.snack_bar_success_message("Operación cancelada correctamente.")
        self.request_barcode()

    def reset_page_default(self):
        self.request_barcode()
