import flet as ft

class GeneralViewsManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.theme_icon_button = None

        self.content = ft.Column(expand=True)
        self.callbacks = ()
        self._layout()

    def set_callbacks(self, callbacks):
        self.callbacks = callbacks

    def _layout(self):
        
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(ft.Icons.POINT_OF_SALE, label="Ventas", padding=5),
                ft.NavigationRailDestination(ft.Icons.STOREFRONT, label="Consultar stock", padding=5),
                ft.NavigationRailDestination(ft.Icons.PRICE_CHANGE, label="Gestionar precios", padding=5),
                ft.NavigationRailDestination(ft.Icons.SETTINGS, label="Ajustes", padding=5)
            ],
            on_change=lambda e: self.change_view(e.control.selected_index)
        )

        self.theme_icon_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Cambiar Tema",
        on_click=self.change_theme
        )

        app_bar = ft.AppBar(
        title=ft.Text("Lotus POS", size=30, weight=ft.FontWeight.BOLD),
        bgcolor=ft.Colors.SURFACE,
        actions=[self.theme_icon_button],
        toolbar_height=40.0
        )

        self.page.add(app_bar,
            ft.Row(
                [rail, ft.VerticalDivider(width=2), ft.Container(self.content, expand=True)],
                expand=True
            )
        )

    def change_theme(self, e):

        self.page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.theme_icon_button.icon = (
            ft.Icons.DARK_MODE
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.LIGHT_MODE
        )

        self.page.update()

    def change_view(self, idx: int):
        if not self.callbacks:
            return
        self.content.controls.clear()
        self.callbacks[idx]()
        self.page.update()