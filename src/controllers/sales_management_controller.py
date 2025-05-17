from src.views.sales_management_views import SalesViewManager
from src.core.sales_management import SaleManagement, SalePersister, Product
from src.exceptions import ProductNotFoundError
from src.utils.logging_config import controller_logger

class SalesManagementController:
    def __init__(self, page, cont):
        controller_logger.info('Program flow started. [SALES MANAGEMENT]')
        self.view = SalesViewManager(page, cont, self)
        self.sale_operation = SaleManagement()

    def get_id(self, barcode):
        try:
            product_id = self.sale_operation.verify_barcode(barcode)
            return product_id
        except ProductNotFoundError as e:
            raise
        except Exception as e:
            controller_logger.exception(f"Unexpected error: {e}")

    def get_product(self, product_id: int) -> Product:
        try:
            product = self.sale_operation.get_full_product(product_id)
            controller_logger.info(f'"{product.product_name}" added to cart.')
            return product
        
        except ProductNotFoundError:
            raise
        except Exception as e:
            controller_logger.exception(f"Unexpected error: {e}")

    def add_new_product(self, product_id, barcode, product_name, available_quantity, customer_price): # Frontend
        self.sale_operation.create_product(product_id, barcode, product_name, available_quantity, customer_price)
    
    def remove_product(self, id_to_cancel):
        """
        Handles the process of removing a product from the cart if the user decides not to buy it.
        """
        controller_logger.info(f'User choice to remove product with ID: {id_to_cancel} from cart.')
        self.sale_operation.cancel_product(id_to_cancel)

    def choose_pay_method(self, method_selected):
        self.sale_operation.set_pay_method(method_selected)
        controller_logger.info(f'Pay method choosed: {method_selected}')

    def complete_sale(self):
        self.sale_operation.build_product_sale()
        self.sale_operation.prepare_sale_summary()
        sale_persister = SalePersister(self.sale_operation)
        sale_persister.confirm_transaction()
        controller_logger.info('[IMPORTANT]: SALE SUCCESSFULLY COMPLETED.\n-')
