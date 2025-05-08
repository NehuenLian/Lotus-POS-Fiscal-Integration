from src.views.check_stock_views import CheckStockViewManager
from src.core.check_stock import CheckStock
from src.exceptions import ProductNotFoundError
from src.utils.logging_config import controller_logger

class StockManagementController:
    def __init__(self, page, cont):
        controller_logger.info('Program flow started. [CHECKING STOCK]')
        self.view = CheckStockViewManager(page, cont, self)
        self.check_stock = CheckStock()

    def check_product(self, barcode):
        try:
            product_name, available_quantity = self.check_stock.search_product(barcode)
            controller_logger.info('[IMPORTANT] CHECK STOCK PROCESS SUCCESSFULLY ENDED.')
            return product_name, available_quantity
        except ProductNotFoundError as e:
            raise
        except Exception as e:
            controller_logger.exception(f"Unexpected error: {e}")