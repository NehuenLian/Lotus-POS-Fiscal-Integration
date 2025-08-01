from sqlalchemy.exc import ArgumentError

from src.business_logic.check_stock import CheckStock
from src.exceptions import ProductNotFoundError
from src.utils.logger import console_logger, controller_logger


class StockManagementController:
    def __init__(self):
        self.check_stock = CheckStock()
        self._view = None

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view) -> None:
        self._view = view

    def get_product(self, barcode: str) -> None:
        try:
            product_id, product_barcode, product_name, available_quantity = self.check_stock.search_product(barcode)
            self._view.display_product(product_id, product_barcode, product_name, available_quantity)
            console_logger.info(f"Product obtained: {product_name}")

        except ProductNotFoundError as e:
            self._view.show_notification_from_controller("Producto no encontrado.")
        except ArgumentError as e:
            self._view.show_notification_from_controller("No hay una base de datos conectada.")
            controller_logger.error(e)
        except Exception as e:
            self._view.show_notification_from_controller("Ocurrió un error desconocido.")
            controller_logger.error(f"Error in StockManagementController.get_product: {e}")