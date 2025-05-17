import flet as ft

class SettingsViewManager:
    def __init__(self, page: ft.Page, cont: ft.Column, settings_controller):
        self.page, self.cont = page, cont
        self.settings_controller = settings_controller
        self.components = UIComponents(self)
        
        self._build_layout()

    def _build_layout(self):
        header = self.components.show_header()
        input_db_utl = self.components.connect_to_other_db_form()

        self.cont.controls = [header, input_db_utl]

        self.page.update()

class UIComponents:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def show_header(self):
        title = ft.Text("Ajustes", size=15, weight=ft.FontWeight.BOLD)
        top_divider = ft.Divider(height=1)

        return ft.Column([title, top_divider])

    def connect_to_other_db_form(self):
        section_title = ft.Text(value="Cambiar de base de datos [Para desarrollador]", size=15)
        section_divider = ft.Divider(height=1)
        db_url_field = ft.TextField(label="Ingrese la URL de la base de datos")
        update_url_button = ft.ElevatedButton("Guardar", on_click=lambda e: self.settings_manager.settings_controller.update_db_url(db_url_field.value))
        disconnect_button = ft.ElevatedButton("Desconectarse", on_click=self.settings_manager.settings_controller.disconnect, bgcolor=ft.Colors.RED)

        return ft.Container(content=ft.Column([
                                            ft.Row([section_title],alignment=ft.MainAxisAlignment.CENTER), 
                                            section_divider, 
                                            ft.Row([db_url_field, update_url_button, disconnect_button])
                                            ]), 
                                        padding=10)
