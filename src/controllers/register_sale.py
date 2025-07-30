from sqlalchemy.exc import ArgumentError

from integration.bridge import invoicing_controller
from src.business_logic.register_sale import (Product, SaleManagement,
                                              SalePersister)
from src.exceptions import InvalidBarcodeError, ProductNotFoundError
from src.utils.logger import console_logger, controller_logger


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
            console_logger.info(f"Product obtained: {product}")
            self._view.create_view_product(product)
        
        except InvalidBarcodeError:
            self._view.show_notification_from_controller("El código de barras contiene caracteres inválidos.")
        except ProductNotFoundError as e:
            self._view.show_notification_from_controller("Producto no encontrado.")
        except ArgumentError as e:
            self._view.show_notification_from_controller("No hay una base de datos conectada.")
            controller_logger.error(e)
        except Exception as e:
            self._view.show_notification_from_controller("Ocurrió un error desconocido.")
            controller_logger.error(f"Error in SalesManagementController.get_product: {e}")
    
    def add_new_product(self, product_id, barcode, product_name, available_quantity, price_excl_vat, price_incl_vat, customer_price): # Frontend
        self.sale_operation.create_product(product_id, barcode, product_name, available_quantity, price_excl_vat, price_incl_vat, customer_price)

    def remove_product(self, id_to_cancel: int) -> None:
        """
        Handle the process of removing a product from the cart if the user decides not to buy it.
        """
        console_logger.info(f'User choice to remove product with ID: {id_to_cancel} from cart.')
        self.sale_operation.cancel_product(id_to_cancel)
    
    def update_product_status(self, product: Product) -> None:
        """
        The DTO 'Product' transitions into a sales-state object, acquiring attributes such as 'subtotal' or 'quantity per product' (subquantity).
        """
        console_logger.info('Product transitions into a sales-state object')
        self.sale_operation.build_product_sale(product)

    def select_pay_method(self, method: str) -> None:
        self.sale_operation.set_pay_method(method)
        console_logger.info(f'Pay method choosed: {method}')

    def complete_sale(self) -> None:
        self.sale_operation.build_product_sale()
        self.sale_operation.prepare_sale_summary()
        sale_persister = SalePersister(self.sale_operation)
        sale_object = self.sale_operation.get_sale_list()
        sale_id = sale_persister.confirm_transaction()
        console_logger.info('[IMPORTANT]: SALE SUCCESSFULLY COMPLETED.\n-')
        self._view.show_notification_from_controller("Venta registrada exitosamente.")

        # Start the invoicing process (separate from the sale registration process)
        invoice_approved = invoicing_controller(sale_object)
        
        if invoice_approved:
            sale_persister.update_fiscal_status(sale_id, True)
        else:
            sale_persister.update_fiscal_status(sale_id, False)

