import flet as ft
import re
from src.exceptions import ProductNotFoundError
from src.utils.flags import FlagManager
from src.views.notifications import SnackBarNotifications

class PriceViewsManager:
    def __init__(self, page: ft.Page, cont: ft.Column, prices_controller):
        self.page, self.cont = page, cont
        self.prices_controller = prices_controller
        self.notification = SnackBarNotifications(page)
        self.components = UIComponents(self)
        self.flags = FlagManager()

        self.data_table = ft.Ref[ft.DataTable]()
        self.barcode_textfield = ft.Ref[ft.TextField]()

        self.current_price_value = None

        self.current_price_label = ft.Ref[ft.Text]()
        self.new_price_textfield = ft.Ref[ft.TextField]()

        self.product_id = None
        self.final_alert_dialog = None

        self._build_first_layout()

    def _build_first_layout(self):
        header = self.components.show_header()
        search = self.components.show_search_controls()
        table = self.components.show_info_table()

        self.cont.controls = [
                            header,
                            search,
                            table,
                        ]

        self.page.update()

    def _build_second_layout(self):
        bottom_divider = self.components.set_bottom_divider()
        update_price_form = self.components.show_price_update_form()
        self.cont.controls.extend([bottom_divider, update_price_form])
        
        self.page.update()

    def add_product_to_table(self, id, product_name, current_price):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(id)), 
                ft.DataCell(ft.Text(product_name)),
                ft.DataCell(ft.Text(f"${current_price}"))
                ])
        
        self.current_price_value = current_price
        self.data_table.current.rows = [new_row]
        self.page.update()

    # Handlers
    def search_product_handler(self, e):
        barcode = self.barcode_textfield.current.value

        if re.fullmatch("[A-Za-z0-9]+", barcode):

            if self.flags.connection_exists:
                try:
                    id, product_name, actual_price = self.prices_controller.check_product(barcode)
                    self.product_id = id
                    self.add_product_to_table(id, product_name, actual_price)
                    self._build_second_layout()
                    
                except ProductNotFoundError:
                    self.notification.snack_bar_error_message("Producto no encontrado.")

            else:
                self.notification.snack_bar_error_message("No se detectó una conexión a una base de datos.")

        else:
            self.notification.snack_bar_error_message("No se permiten caracteres especiales.")

    def alert_dialog_handler(self):

        self.final_alert_dialog = self.components.confirm_changes_modal()

        self.page.open(self.final_alert_dialog)

    def confirm_changes_handler(self, e):
        self.prices_controller.update_price(self.product_id, self.new_price_textfield.current.value)
        self.notification.snack_bar_success_message("Precio actualizado correctamente.")
        self.page.close(self.final_alert_dialog)
        self.reset_page_default()

    def update_price_handler(self, e):

        try:
            self.new_price = float(self.new_price_textfield.current.value)
        except ValueError:
            self.notification.snack_bar_error_message("Por favor, ingrese un valor.")

        else:
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

class UIComponents:
    def __init__(self, prices_views_manager):
        self.prices_views_manager = prices_views_manager

    def show_header(self):
        title = ft.Text("Gestionar Precios", size=15, weight=ft.FontWeight.BOLD)
        top_divider = ft.Divider(height=1)

        return ft.Column([title, top_divider])
    
    def show_search_controls(self):
        barcode_field =  ft.TextField(ref=self.prices_views_manager.barcode_textfield, label="Ingrese el código del producto...", width=300 ,on_submit=self.prices_views_manager.search_product_handler)
        button = ft.ElevatedButton("Obtener", on_click=self.prices_views_manager.search_product_handler)

        return ft.Row([barcode_field, button], spacing=20)
    
    def show_info_table(self):
        table = ft.DataTable(ref=self.prices_views_manager.data_table,
        border=ft.border.all(2, ft.Colors.BLUE_GREY_200),
        vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE_GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_400),
            columns = [
                ft.DataColumn(ft.Text(value="ID")),
                ft.DataColumn(ft.Text(value="Nombre del Producto")),
                ft.DataColumn(ft.Text(value="Precio actual")),
            ])
        
        return ft.Container(content=ft.Column([ft.Row([table], alignment=ft.MainAxisAlignment.CENTER)], scroll="auto"), expand=True)
    
    def set_bottom_divider(self):
        return ft.Divider(height=1)
    
    def show_price_update_form(self):
        current_price = ft.Text(ref=self.prices_views_manager.current_price_label, value=f"Precio actual: ${self.prices_views_manager.current_price_value}")
        new_price_textfield = ft.TextField(ref=self.prices_views_manager.new_price_textfield, label="Nuevo precio...", 
                                        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(\.\d*)?$"))
        
        update_price_button = ft.ElevatedButton("Actualizar", on_click=self.prices_views_manager.update_price_handler)

        return ft.Column([ft.Row([current_price,]), ft.Row([new_price_textfield, update_price_button])])
 
    def confirm_changes_modal(self):
        return ft.AlertDialog(
        modal=True,
        content=ft.Text("¿Confirmar cambios?"),
        actions=[
            ft.TextButton("Confirmar", on_click=self.prices_views_manager.confirm_changes_handler),
            ft.TextButton("Cancelar", on_click=self.prices_views_manager.cancel_operation),
        ],
        actions_alignment=ft.MainAxisAlignment.END)