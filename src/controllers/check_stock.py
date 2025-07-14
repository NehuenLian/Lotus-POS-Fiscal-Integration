from src.business_logic.check_stock import CheckStock
from src.exceptions import ProductNotFoundError
from src.utils.logger_config import controller_logger


class StockManagementController:
    def __init__(self):
        controller_logger.info('Program flow started. [CHECKING STOCK]')
        self._view = None
        self.check_stock = CheckStock()

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view):
        self._view = view

    def manage_check_stock(self):
        print("Hola, estas en check_stock")
        barcode = self.view.request_barcode()
        controller_logger.info(f'User input barcode "{barcode}".')
        try:
            product_name, available_quantity = self.check_stock.search_product(barcode)
            self.view.display_product(product_name, available_quantity)
            controller_logger.info('[IMPORTANT] CHECK STOCK PROCESS SUCCESSFULLY ENDED.')
        except ProductNotFoundError as e:
            print("Producto no encontrado.")
        except Exception as e:
            print(f"Error inesperado: {e}")