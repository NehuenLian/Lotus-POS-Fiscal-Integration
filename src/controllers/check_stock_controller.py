from src.views.check_stock_views import CheckStockViewManager
from src.core.check_stock import CheckStock
from src.exceptions import ProductNotFoundError
from src.utils.logging_config import controller_logger

class StockManagementController:
    def __init__(self):
        controller_logger.info('Program flow started. [CHECKING STOCK]')
        self.view = CheckStockViewManager()
        self.check_stock = CheckStock()

    def manage_check_stock(self):
        self.view.show_message("El usuario eligió consultar stock.")
        barcode = self.view.request_barcode()
        controller_logger.info(f'User input barcode "{barcode}".')
        try:
            product_name, available_quantity = self.check_stock.search_product(barcode)
            self.view.display_product(product_name, available_quantity)
            controller_logger.info('[IMPORTANT] CHECK STOCK PROCESS SUCCESSFULLY ENDED.')
        except ProductNotFoundError as e:
            self.view.show_message("Producto no encontrado.")
        except Exception as e:
            self.view.show_message(f"Error inesperado: {e}")