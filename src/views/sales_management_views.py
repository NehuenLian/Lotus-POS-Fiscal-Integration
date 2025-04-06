import re

class SalesViewManager:
    def __init__(self):
        pass

    def show_message(self, message):
        print(message)

    def show_total(self, amount):
        self.show_message(f"Total: ${amount}")

    def show_total_quantity(self, total_quantity):
        self.show_message(f"Cantidad total de productos: {total_quantity}")

    def back_menu(self):
        self.show_message("-"*30)
        self.show_message("Volviendo al menú...")

    def display_product(self, products):
        self.show_message("====" * 22)
        self.show_message(f"Su compra:")
        for p in products:
            self.show_message(f"ID: {p['id']} | {p['product_name']} | Precio: ${p['customer_price']}.")

    def display_sale(self, products):
        position = 0
        for _ in products:
            self.show_message(products[position])
            position += 1


    def request_barcode(self): # TODO: Textfield
        while True:
            barcode = input("Si desea volver, presione 'V'.\nIngrese un código o ingrese 'C' para continuar con la venta: ")
            if barcode.lower == 'c':
                break
            elif re.fullmatch("[A-Za-z0-9]+", barcode):
                barcode = barcode.upper()
                return barcode
            else:
                self.show_message("Entrada inválida, no se permiten caracteres especiales.")

    def choice_product_for_cancel(self): # TODO: Textfield
        while True:
            id_to_cancel = input("Ingrese la id del producto que desea cancelar: ")
            if id_to_cancel.isdigit():
                return int(id_to_cancel)
            else:
                self.show_message("La ID no puede ser una letra.")


    def continue_with_sale(self): # TODO: Button
        while True:
            try:
                continue_input = int(input("Presione 1 para continuar con la venta o 2 para anular otro producto: "))
                return continue_input
            except ValueError:
                self.show_message(f"Ingresa una entrada válida.")

    def ask_pay_method(self): # TODO: Button
        pay_methods = ["Efectivo", "Transferencia"]

        while True:
            choose_pay_method = int(input(f"Seleccionar método de pago 0({pay_methods[0]}) o 1({pay_methods[1]}): "))
            if choose_pay_method in (0, 1):
                method_selected = pay_methods[choose_pay_method]
                break

        return method_selected
    
    def cancel_product_question(self): # TODO: Button
        while True:
            choice = input("Desea anular un producto? S/N: ")
            if choice.lower() in ('s', 'n'):
                return choice