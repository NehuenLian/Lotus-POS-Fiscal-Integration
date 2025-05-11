import flet as ft

class GeneralViewsManager:
    def __init__(self, page: ft.Page):
        self.page = page
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
                ft.NavigationRailDestination(ft.Icons.POINT_OF_SALE, label="Ventas"),
                ft.NavigationRailDestination(ft.Icons.STOREFRONT, label="Consultar stock"),
                ft.NavigationRailDestination(ft.Icons.PRICE_CHANGE, label="Gestionar precios"),
                ft.NavigationRailDestination(ft.Icons.SETTINGS, label="Ajustes")
            ],
            on_change=lambda e: self.change_view(e.control.selected_index)
        )

        self.page.add(
            ft.Row(
                [rail, ft.VerticalDivider(width=1), ft.Container(self.content, expand=True)],
                expand=True
            )
        )

    def change_view(self, idx: int):
        if not self.callbacks:
            return
        self.content.controls.clear()
        self.callbacks[idx]()
        self.page.update()