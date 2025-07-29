from sqlalchemy.exc import ArgumentError

from src.business_logic.manage_prices import PriceManagement
from src.exceptions import (InvalidPriceError, ProductNotFoundError,
                            TransactionIntegrityError)
from src.utils.logger import console_logger, controller_logger


class PricesManagementController:
    def __init__(self):
        self.change_prices = PriceManagement()
        self._view = None

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view) -> None:
        self._view = view

    def get_product(self, barcode: str) -> int:
        try:
            product_id, product_barcode, product_name, available_quantity = self.change_prices.search_product(barcode)
            self._view.display_product(product_id, product_barcode, product_name, available_quantity)
            console_logger.info(f"Product obtained: {product_name}")
            return product_id

        except ProductNotFoundError as e:
            self._view.show_notification_from_controller("Producto no encontrado.")
        except ArgumentError as e:
            self._view.show_notification_from_controller("No hay una base de datos conectada.")
            controller_logger.error(e)
        except Exception as e:
            self._view.show_notification_from_controller("Ocurrió un error desconocido.")
            controller_logger.error(f"Error in PricesManagementController.get_product: {e}")
    
    def update_price(self, product_id: int, new_price: float):
        try:
            self.change_prices.update_prices(product_id, new_price)
            self._view.show_notification_from_controller("El cambio de precio se realizó correctamente.")

        except InvalidPriceError:
            self._view.show_notification_from_controller("El nuevo precio no puede ser negativo o menor a $1.")
        except TransactionIntegrityError as e:
            self._view.show_notification_from_controller("Ocurrió un error al actualizar el precio en el registro, inténtelo de nuevo.")
            controller_logger.error(e)
        except ArgumentError as e:
            self._view.show_notification_from_controller("No hay una base de datos conectada.")
            controller_logger.error(e)
        except Exception as e:
            self._view.show_notification_from_controller("Ocurrió un error desconocido.")
            controller_logger.error(f"Error in PricesManagementController.update_price: {e}")
