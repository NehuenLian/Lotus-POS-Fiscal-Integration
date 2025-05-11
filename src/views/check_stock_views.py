import flet as ft
import re
from src.exceptions import ProductNotFoundError

class CheckStockViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, stock_controller):
        self.page, self.cont = page, cont
        self.stock_controller = stock_controller
        self.notification = Notifications(page)
        self.widgets = Widgets(self)

        self.data_table = ft.Ref[ft.DataTable]()

        self.barcode_textfield = ft.Ref[ft.TextField]()

        self._build_layout()

    def _build_layout(self):
        title = self.widgets.show_title()
        top_divider = self.widgets.show_top_divider()
        barcode_textfield = self.widgets.show_barcode_textfield()
        search_button = self.widgets.show_search_button()
        table = self.widgets.show_info_table()

        self.cont.controls = [
                            title,
                            top_divider,
                            barcode_textfield,
                            search_button,
                            table,
                        ]

    def add_product_to_table(self, id, product_name):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(id)), 
                ft.DataCell(ft.Text(product_name)),
                ])

        self.data_table.current.rows = [new_row]
        self.page.update()

    # Handler
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.current.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):
            try:
                product_name, available_quantity = self.stock_controller.check_product(barcode)
                self.add_product_to_table(product_name, available_quantity)
            except ProductNotFoundError:
                self.notification.snack_bar_error_message("Producto no encontrado.")
        else:
            self.notification.snack_bar_error_message("No se permiten caracteres especiales.")

class Widgets:
    def __init__(self, stock_views_manager):
        self.stock_views_manager = stock_views_manager

    def show_title(self):
        return ft.Row([ft.Text("Consultar Stock", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER)
    
    def show_top_divider(self):
        return ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)
    
    def show_barcode_textfield(self):
        return ft.TextField(ref=self.stock_views_manager.barcode_textfield, label="Ingrese el código del producto...", width=300 ,on_submit=self.stock_views_manager.search_product_handler)
    
    def show_search_button(self):
        return ft.ElevatedButton("Obtener", on_click=self.stock_views_manager.search_product_handler, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
    
    def show_info_table(self):
        table = ft.DataTable(ref=self.stock_views_manager.data_table,
            bgcolor=ft.Colors.BLUE_GREY_900,
            border=ft.border.all(2, ft.Colors.BLUE_GREY_500),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="Nombre del Producto", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text(value="Cantidad disponible", color=ft.Colors.WHITE)),
            ])
        
        return ft.Container(content=ft.Column([table], scroll="auto"), height=300, border_radius=5, border=ft.border.all(2, ft.Colors.BLACK), padding=5)
    
class Notifications:
    def __init__(self, page):
        self.page = page
 
    #  Notifications: display popup messages for error or success feedback in the UI
    def snack_bar_error_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message, 
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.RED))