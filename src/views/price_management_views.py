import flet as ft
import re
from src.exceptions import ProductNotFoundError

class PriceViewsManager:
    def __init__(self, page: ft.Page, cont: ft.Column, prices_controller):
        self.page, self.cont = page, cont
        self.prices_controller = prices_controller
        self.notification = Notifications(page)
        self.widgets = Widgets(self)

        self.data_table = ft.Ref[ft.DataTable]()
        self.barcode_textfield = ft.Ref[ft.TextField]()

        self.current_price_label = ft.Ref[ft.Text]()
        self.new_price_textfield = ft.Ref[ft.TextField]()

        self.product_id = None
        self.final_alert_dialog = None

        self._build_first_layout()

    def _build_first_layout(self):
        title = self.widgets.show_title()
        top_divider = self.widgets.show_top_divider()
        barcode_textfield = self.widgets.show_barcode_textfield()
        search_button = self.widgets.show_search_button()
        table = self.widgets.show_info_table()
        current_price = self.widgets.show_current_product_price()

        self.cont.controls = [
                            title,
                            top_divider,
                            barcode_textfield,
                            search_button,
                            table,
                            current_price
                        ]

        self.page.update()

    def _build_second_layout(self):
        new_price_textfield = self.widgets.show_new_price_textfield()
        update_price_button = self.widgets.set_new_price()

        self.cont.controls.extend([
                            new_price_textfield,
                            update_price_button,
                            ])
        
        self.page.update()

    def add_product_to_table(self, id, product_name, current_price):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(id)), 
                ft.DataCell(ft.Text(product_name)),
                ft.DataCell(ft.Text(f"${current_price}"))
                ])

        self.current_price_label.current.value = f"Precio actual: ${current_price}"
        self.data_table.current.rows = [new_row]
        self.page.update()

    # Handlers
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.current.value
        if re.fullmatch("[A-Za-z0-9]+", barcode):
            try:
                id, product_name, actual_price = self.prices_controller.check_product(barcode)
                self.product_id = id
                self.add_product_to_table(id, product_name, actual_price)
                self._build_second_layout()
            except ProductNotFoundError:
                self.notification.snack_bar_error_message("Producto no encontrado.")
        else:
            self.notification.snack_bar_error_message("No se permiten caracteres especiales.")

    def alert_dialog_handler(self):
        self.final_alert_dialog = self.widgets.confirm_changes_modal()
        self.page.open(self.final_alert_dialog)

    def confirm_changes_handler(self, e):
        self.prices_controller.update_price(self.product_id, self.new_price_textfield.current.value)
        self.notification.snack_bar_success_message("Precio actualizado correctamente.")
        self.page.close(self.final_alert_dialog)
        self.reset_page_default()

    def update_price_handler(self, e):
        self.new_price = float(self.new_price_textfield.current.value)
        if self.new_price > 0:
            self.alert_dialog_handler()
        elif self.new_price <= 0:
            self.notification.snack_bar_error_message("No se puede ingresar un precio menor a $0.")

    # Aux
    def cancel_operation(self, e):
        self.notification.snack_bar_success_message("Operación cancelada.")
        self.page.close(self.final_alert_dialog)
        self.reset_page_default()

    def reset_page_default(self):
        self._build_first_layout()

class Widgets:
    def __init__(self, prices_views_manager):
        self.prices_views_manager = prices_views_manager

    def show_title(self):
        return ft.Row([ft.Text("Gestionar Precios", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.CENTER)
    
    def show_top_divider(self):
        return ft.Divider(height=20, thickness=1, color=ft.Colors.GREY_600)
    
    def show_barcode_textfield(self):
        return ft.TextField(ref=self.prices_views_manager.barcode_textfield, label="Ingrese el código del producto...", 
                            width=300 ,on_submit=self.prices_views_manager.search_product_handler)
    
    def show_search_button(self):
        return ft.ElevatedButton("Obtener", on_click=self.prices_views_manager.search_product_handler, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
    
    def show_info_table(self):
        table = ft.DataTable(ref=self.prices_views_manager.data_table,
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
        
        return ft.Container(content=ft.Column([table], scroll="auto"), height=300, border_radius=5, border=ft.border.all(2, ft.Colors.BLACK), padding=5)
    
    def show_current_product_price(self):
        return ft.Text(ref=self.prices_views_manager.current_price_label, value=f"Precio actual: $0")
    
    def show_new_price_textfield(self):
        return ft.TextField(ref=self.prices_views_manager.new_price_textfield, label="$ ", input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(\.\d*)?$"))
    
    def set_new_price(self):
        return ft.ElevatedButton("Actualizar", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=self.prices_views_manager.update_price_handler)
    
    def confirm_changes_modal(self):
        return ft.AlertDialog(
        modal=True,
        content=ft.Text("¿Confirmar cambios?"),
        actions=[
            ft.TextButton("Confirmar", on_click=self.prices_views_manager.confirm_changes_handler),
            ft.TextButton("Cancelar", on_click=self.prices_views_manager.cancel_operation),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog cerrado"),
    )

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
    
    def snack_bar_success_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message,
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.GREEN))