class GeneralViewsManager:
    def __init__(self):
        pass

    def show_menu(self):
        self.show_message(" -- Si desea consultar stock, inserte 1 -- ")
        self.show_message(" -- Si desea insertar una venta, inserte 2 -- ")
        self.show_message(" -- Si desea hacer gestión de precios, inserte 3 -- ")
        self.show_message("-"*30)
        self.show_message(" -- O si desea salir, presione Ctrl + C. -- ")

    def show_message(self, message):
        print(message)

    def input_message(self, input_text):
        data = input(input_text)
        return data
    
    def back_menu(self):
        self.show_message("-"*30)
        self.show_message("Volviendo al menú...")


    def get_user_choice(self) -> str:  # TODO: Textfield
        while True:
            choice = str(input("Insertar: "))
            return choice

    def request_barcode(self)-> str:  # TODO: Textfield
        while True:
            insert_code = input("Ingrese el código del producto o presione V para volver: ")
            return insert_code
