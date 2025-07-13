from src.business_logic.manage_prices import PriceManagement
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logging_config import controller_logger
from src.views.manage_prices import PriceViewsManager


class PricesManagementController:
    def __init__(self):
        self.view = PriceViewsManager()
        self.change_prices = PriceManagement()

        controller_logger.info('Program flow started. [PRICES MANAGEMENT]')

    def get_barcode(self) -> list:
        self.view.show_message("El usuario eligió gestionar precios.")

        getting_product = True
        while getting_product:
            try:
                    barcode = self.view.request_barcode()
                    if barcode:
                        [id, product_name, actual_price] = self.change_prices.search_product(barcode)
                        product_properties = [id, product_name, actual_price]
                        getting_product = False
                        controller_logger.info(f'Get barcode process successfully ended. User input barcode "{barcode}" Actual price: {actual_price}.')
                        return product_properties
            except ProductNotFoundError:
                    self.view.show_message("Producto no encontrado.")
            except Exception as e:
                    self.view.show_message(f"Error desconocido: {e}")

    def show_product_info(self, product_properties):
        self.view.display_product(product_properties[1], product_properties[2])

    def choose_new_price(self, product_properties) -> float:
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

    def manage_update_prices_process(self):
        print("Hola, estas en manage_prices")
