from src.business_logic.price_management import PriceManagement
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logging_config import controller_logger
from src.views.price_management_views import PriceViewsManager


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
        while True:
            product_properties = self.get_barcode()
            self.show_product_info(product_properties)
            new_price = self.choose_new_price(product_properties)
            confirm_choice = self.confirming_process()
            if confirm_choice.lower() == 's':
                controller_logger.info('Changes confirmed.')
                self.update_price(product_properties, new_price)
                self.view.show_message(f"El precio de {product_properties[1]} se actualizó correctamente.")
                controller_logger.info(f'[IMPORTANT] UPDATE SUCCESSFULLY COMPLETED.\n-')
                self.view.back_menu()
                break
            elif confirm_choice.lower() == 'n':
                controller_logger.info(f'[IMPORTANT] Changes denied. PROCESS ABORTED.\n-')
                self.view.show_message("Cancelando operación...")
                self.view.back_menu()
                break
            else: # TODO: Remove this "else" when the graphical interface is implemented.
                print("Ingresa una entrada válida")
