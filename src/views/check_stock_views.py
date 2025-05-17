import re

import flet as ft

from src.exceptions import ProductNotFoundError
from src.utils.flags import FlagManager
from src.views.ui_notifications import SnackBarNotifications


class CheckStockViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, stock_controller):
        self.page, self.cont = page, cont
        self.stock_controller = stock_controller
        self.notification = SnackBarNotifications(page)
        self.components = UIComponents(self)
        self.flags = FlagManager()

        self.data_table = ft.Ref[ft.DataTable]()

        self.barcode_textfield = ft.Ref[ft.TextField]()

        self._build_layout()

    def _build_layout(self):
        header = self.components.show_header()
        search = self.components.show_search_controls()
        table = self.components.show_info_table()

        self.cont.controls = [
                            header,
                            search,
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
            if self.flags.connection_exists:
                try:
                    product_name, available_quantity = self.stock_controller.check_product(barcode)
                    self.add_product_to_table(product_name, available_quantity)

                except ProductNotFoundError:
                    self.notification.snack_bar_error_message("Producto no encontrado.")
                    
            else:
                self.notification.snack_bar_error_message("No se detectó una conexión a una base de datos.")

        else:
            self.notification.snack_bar_error_message("No se permiten caracteres especiales.")

class UIComponents:
    def __init__(self, stock_views_manager):
        self.stock_views_manager = stock_views_manager

    def show_header(self):
        title = ft.Text("Consultar Stock", size=15, weight=ft.FontWeight.BOLD)
        top_divider = ft.Divider(height=1)

        return ft.Column([title, top_divider])
    
    def show_search_controls(self):
        barcode_field =  ft.TextField(ref=self.stock_views_manager.barcode_textfield, label="Ingrese el código del producto...", width=300 ,on_submit=self.stock_views_manager.search_product_handler)
        button = ft.ElevatedButton("Obtener", on_click=self.stock_views_manager.search_product_handler)

        return ft.Row([barcode_field, button], spacing=20)
    
    def show_info_table(self):
        table = ft.DataTable(ref=self.stock_views_manager.data_table,
        border=ft.border.all(2, ft.Colors.BLUE_GREY_200),
        vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="Nombre del Producto")),
                ft.DataColumn(ft.Text(value="Cantidad disponible")),
            ])
        
        return ft.Container(content=ft.Column([ft.Row([table], alignment=ft.MainAxisAlignment.CENTER)], scroll="auto"), expand=True)