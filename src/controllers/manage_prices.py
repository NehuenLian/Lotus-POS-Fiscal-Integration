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

    def get_product(self, barcode: str) -> None:
        try:
            product_id, product_barcode, product_name, available_quantity = self.change_prices.search_product(barcode)
            self._view.display_product(product_id, product_barcode, product_name, available_quantity)

        except ProductNotFoundError as e:
            print("Producto no encontrado.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def choose_new_price(self, product_properties: list) -> float:
        new_price = self.view.set_new_price()
        self.view.display_prices(product_properties[2], new_price)
        controller_logger.info(f'New price: ${new_price}')

        return new_price
    
    def confirming_process(self) -> str:
        confirm_choice = self.view.confirm_changes_qt()
        return confirm_choice
    
    def update_price(self, product_properties, new_price):
        try:
            self.change_prices.update_prices(product_properties[0], new_price)
            self.view.show_message("El cambio de precio se realizó correctamente.")

        except TransactionIntegrityError as e:
            self.view.show_message(f"Ocurrió un error al actualizar el precio en el registro, inténtalo de nuevo.")
        except Exception as e:
            self.view.show_message(f"Error desconocido: {e}")