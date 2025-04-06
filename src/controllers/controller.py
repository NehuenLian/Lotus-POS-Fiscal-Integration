from src.controllers.check_stock_controller import StockManagementController
from src.controllers.price_management_controller import PricesManagementController
from src.controllers.sales_management_controller import SalesManagementController
from src.database import connection
from src.utils.logging_config import controller_logger
from src.views.general_views import GeneralViewsManager


class MainController:
    def __init__(self):
        self.ui = GeneralViewsManager()

    def connect_to_db(self):
        try:
            connection.connect()
            self.ui.show_message("Conexión exitosa src/controllers/controller.py")
        except:
            self.ui.show_message(f"Ocurrió un error al conectarse a la base de datos.")
            raise Exception

    def handle_user_choices(self, choice):
        if choice == '1':
            a = StockManagementController()
            a.manage_check_stock()
        elif choice == '2':
            b = SalesManagementController()
            b.manage_sale_process()
        elif choice == '3':
            c = PricesManagementController()
            c.manage_update_prices_process()
        else:
            self.ui.show_message("Ingresa una entrada válida.")
            self.ui.show_message("=============================")

    def execute(self):
        try:
            self.connect_to_db()
        except Exception as e:
            self.ui.show_message(f"Algo falló al intentar conectarse a la base de datos. Detalles: {e}")
        while True:
            self.ui.show_menu()
            choice = self.ui.get_user_choice()
            self.handle_user_choices(choice)
