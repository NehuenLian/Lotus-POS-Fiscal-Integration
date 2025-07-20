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
            self._view.show_notification_from_controller("Producto no encontrado.")
        except Exception as e:
            self._view.show_notification_from_controller("Ocurrió un error desconocido.")
            controller_logger(e)
    
    def add_new_product(self, product_id, barcode, product_name, available_quantity, customer_price): # Frontend
        self.sale_operation.create_product(product_id, barcode, product_name, available_quantity, customer_price)

    def remove_product(self, id_to_cancel: int) -> None:
        """
        Handle the process of removing a product from the cart if the user decides not to buy it.
        """
        controller_logger.info(f'User choice to remove product with ID: {id_to_cancel} from cart.')
        self.sale_operation.cancel_product(id_to_cancel)
    
    def update_product_status(self, product: Product) -> None:
        """
        The DTO 'Product' transitions into a sales-state object, acquiring attributes such as 'subtotal' or 'quantity per product' (subquantity).
        """
        controller_logger.info('Product transitions into a sales-state object')
        self.sale_operation.build_product_sale(product)

    def select_pay_method(self, method: str) -> None:
        self.sale_operation.set_pay_method(method)
        controller_logger.info(f'Pay method choosed: {method}')

    def complete_sale(self) -> None:
        self.sale_operation.prepare_sale_summary()
        sale_persister = SalePersister(self.sale_operation)
        sale_persister.confirm_transaction()
        controller_logger.info('[IMPORTANT]: SALE SUCCESSFULLY COMPLETED.\n-')
        self._view.show_notification_from_controller("Venta registrada exitosamente.")



