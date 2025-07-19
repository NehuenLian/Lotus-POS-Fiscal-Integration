from src.business_logic.manage_prices import PriceManagement
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logger_config import controller_logger


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
            return product_id

        except ProductNotFoundError as e:
            print("Producto no encontrado.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def update_price(self, product_id: int, new_price: float):
        try:
            self.change_prices.update_prices(product_id, new_price)
            print("El cambio de precio se realizó correctamente.")

        except TransactionIntegrityError as e:
            print(f"Ocurrió un error al actualizar el precio en el registro, inténtalo de nuevo.")
        except Exception as e:
            print(f"Error desconocido: {e}")