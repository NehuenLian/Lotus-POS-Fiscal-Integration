import re


class PriceViewsManager:
    def __init__(self):
        pass

    def show_message(self, message):
        print(message)

    def display_product(self, name, actual_price):
        self.show_message(f"Nombre del producto: {name} | Precio: {actual_price}")

    def display_prices(self, actual_price, new_price):
        self.show_message(f"Precio anterior: {actual_price}, Nuevo precio: {new_price}")

    def back_menu(self):
        self.show_message("-"*30)
        self.show_message("Volviendo al menú...")
        

    def request_barcode(self) -> str: # TODO: Textfield
        while True:
            barcode = input("Ingrese el código del producto o presione V para volver: ")
            if re.fullmatch("[A-Za-z0-9]+", barcode):
                barcode = barcode.upper()
                return barcode
            else:
                self.show_message("Entrada inválida, no se permiten caracteres especiales.")

    def set_new_price(self) -> float: # TODO: Textfield
        while True:
            try:
                num = input("Ingrese el nuevo precio: ")
                new_price = float(num)
                if new_price > 0:
                    return new_price
                else:
                    self.show_message("No se puede ingresar un precio menor a $0.")
            except ValueError:
                self.show_message("No se puede ingresar letras o caracteres especiales.")


    def confirm_changes_qt(self, user_choice=None):  #TODO: Textfield
        user_choice = input("¿Confirmar? S/N: ")
        return user_choice.lower()
