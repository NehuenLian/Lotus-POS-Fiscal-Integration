import flet as ft
from src.controllers.controller import MainController

def main(page: ft.Page):
    MainController(page)

if __name__ == "__main__":
    ft.app(target=main)