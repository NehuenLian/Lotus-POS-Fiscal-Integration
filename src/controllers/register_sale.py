from src.business_logic.register_sale import (Product, SaleManagement,
                                              SalePersister)
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logger_config import controller_logger


class SalesManagementController:
    def __init__(self):
        self.sale_operation = SaleManagement()
        self._view = None

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view) -> None:
        self._view = view

    def get_product(self, barcode: str) -> None:
        try:
            product = self.sale_operation.get_full_product(barcode)
            self._view.create_view_product(product)

        except ProductNotFoundError as e:
            print("Producto no encontrado.")
        except Exception as e:
            print(f"Error inesperado en get_product (controlador de register_sale): {e}")

    def remove_soon(self, barcode):
        print(f"Obteniendo producto... {barcode}")

    def get_barcode(self) -> int:
        self.view.show_message("El usuario eligió gestionar ventas.")
        barcode = self.view.request_barcode()
        controller_logger.info(f'User input barcode "{barcode}".')

        return barcode

    def get_id(self, barcode):
        try:
            product_id = self.sale_operation.verify_barcode(barcode)
            return product_id
        
        except ProductNotFoundError as e:
            self.view.show_message("Producto no encontrado.")
        except Exception as e:
            self.view.show_message(f"Error inesperado: {e}")
    
    def add_new_product(self, product_id, barcode, product_name, available_quantity, customer_price): # Frontend
        self.sale_operation.create_product(product_id, barcode, product_name, available_quantity, customer_price)

    def remove_product(self, id_to_cancel):
        """
        Handle the process of removing a product from the cart if the user decides not to buy it.
        """
        controller_logger.info(f'User choice to remove product with ID: {id_to_cancel} from cart.')
        self.sale_operation.cancel_product(id_to_cancel)
    
    def update_product_status(self, product: Product):
        controller_logger.info('Product transitions into a sales-state object')
        """
        The DTO 'Product' transitions into a sales-state object, acquiring attributes such as 'subtotal' or 'quantity per product' (subquantity).
        """
        self.sale_operation.build_product_sale(product)

    def show_sale_info(self, amount: float, total_quantity: int):
        self.view.show_total(amount)
        self.view.show_total_quantity(total_quantity)

    def choose_pay_method(self):
        method_selected = self.view.ask_pay_method()
        self.sale_operation.set_pay_method(method_selected)
        controller_logger.info(f'Pay method choosed: {method_selected}')

    def complete_sale(self):
        self.sale_operation.prepare_sale_summary()
        sale_persister = SalePersister(self.sale_operation)
        sale_persister.confirm_transaction()
        controller_logger.info('[IMPORTANT]: SALE SUCCESSFULLY COMPLETED.\n-')



