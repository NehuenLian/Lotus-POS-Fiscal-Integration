from src.views.price_management_views import PriceViewsManager
from src.core.price_management import PriceManagement
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logging_config import controller_logger

class PricesManagementController:
    def __init__(self, page, cont):
        self.view = PriceViewsManager(page, cont, self)
        self.change_prices = PriceManagement()

        controller_logger.info('Program flow started. [PRICES MANAGEMENT]')

    def check_product(self, barcode):
        try:
            id, product_name, actual_price = self.change_prices.search_product(barcode)
            self.view.display_product(id, product_name, actual_price)
            controller_logger.info(f'Get barcode process successfully ended. User input barcode "{barcode}" Actual price: ${actual_price}.')
            return id, product_name, actual_price
        except ProductNotFoundError as e:
            raise
        except Exception as e:
            controller_logger.exception(f"Unexpected error: {e}")
    
    def update_price(self, id, new_price):
        try:
            self.change_prices.update_prices(id, new_price)
            self.view.snack_bar_success_message("El cambio de precio se realizó correctamente.")
        except TransactionIntegrityError as e:
            self.view.snack_bar_error_message(f"Ocurrió un error al actualizar el precio en el registro, inténtelo de nuevo.")
        except Exception as e:
            controller_logger.exception(f"Unexpected error: {e}")