import flet as ft
import re
from src.exceptions import ProductNotFoundError

class CheckStockViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, stock_controller):
        self.page, self.cont = page, cont
        self.stock_controller = stock_controller

        """
        Inicializamos los componentes de la pagina en vacio 
        de esta forma, seran "globales" para toda la clase
        pudiendo agregarlos a cualquier metodo cuando quiera actualizar la vista
        """

        self.title = None
        self.divider = None
        self.barcode = None
        self.barcode_textfield = None
        self.button = None
        self.data_table = None
        self.error_message = None

        self.data_table_row = None

        self.input_and_button_row = None

        self.request_barcode()

    def snack_bar_error_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message, 
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.RED))

    def request_barcode(self):
        self.title = ft.Row([ft.Text("Consultar Stock", 
                                     size=30, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER)
        
        self.divider = ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)
        self.barcode_textfield = ft.TextField(label="Ingrese el código del producto...", on_submit=self.on_click_handler)
        self.button = ft.ElevatedButton("Consultar", on_click=self.on_click_handler, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        self.input_and_button_row = ft.Row([self.barcode_textfield, self.button], alignment=ft.MainAxisAlignment.CENTER)

        self.cont.controls = [self.title, self.divider, self.input_and_button_row]

    def on_click_handler(self, e):
        barcode = self.barcode_textfield.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):
            try:
                product_name, available_quantity = self.stock_controller.check_product(barcode)
                self.display_product(product_name, available_quantity)
            except ProductNotFoundError:
                self.snack_bar_error_message("Producto no encontrado.")
        else:
            self.snack_bar_error_message("No se permiten caracteres especiales.")

    def display_product(self, product_name, available_quantity):

        self.data_table = ft.DataTable(
            bgcolor=ft.Colors.BLUE_GREY_900,
            border=ft.border.all(2, ft.Colors.BLUE_GREY_500),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="Nombre del Producto", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Cantidad disponible", color=ft.Colors.WHITE)),
            ])

        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(product_name)), 
                ft.DataCell(ft.Text(available_quantity))
                ])
        
        self.data_table_row = ft.Row([self.data_table], ft.MainAxisAlignment.CENTER)

        self.data_table.rows.append(new_row)
        self.cont.controls = [self.title, self.divider, self.input_and_button_row, self.data_table_row]
        self.page.update()
