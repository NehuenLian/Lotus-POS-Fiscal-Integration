import re


class CheckStockViewManager:
    def __init__(self):
        pass

    def show_message(self, message):
        print(message)
        
    def display_product(self, product_name, available_quantity):
        self.show_message(f"Nombre del producto: {product_name} | Cantidad disponible: {available_quantity}")

    def back_menu(self):
        self.show_message("-"*30)
        self.show_message("Volviendo al menú...")


    def request_barcode(self):  # TODO: Textfield
        while True:
            barcode = input("Ingrese el código del producto o presione V para volver: ")
            if re.fullmatch("[A-Za-z0-9]+", barcode):
                barcode = barcode.upper()
                return barcode
            else:
                self.show_message("Entrada inválida, no se permiten caracteres especiales.")
