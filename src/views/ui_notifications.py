import flet as ft

class SnackBarNotifications:
    def __init__(self, page):
        self.page = page
 
    #  Notifications: display popup messages for error or success feedback in the UI
    def snack_bar_error_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message, 
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.RED, duration=2000))
    
    def snack_bar_neutral_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message, 
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.GREY_400, duration=2000))
    
    def snack_bar_success_message(self, message):
        return self.page.open(ft.SnackBar(ft.Text(value=message,
                                                color=ft.Colors.WHITE, 
                                                weight=ft.FontWeight.BOLD, 
                                                text_align=ft.TextAlign.CENTER,
                                                size=20
                                                ), bgcolor=ft.Colors.GREEN, duration=1000))