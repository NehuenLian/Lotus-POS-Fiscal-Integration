from src.business_logic.sales import Product, SaleManagement, SalePersister
from src.exceptions import ProductNotFoundError, TransactionIntegrityError
from src.utils.logging_config import controller_logger
from src.views.sales import SalesViewManager


class SalesManagementController:
    def __init__(self):
        controller_logger.info('Program flow started. [SALES MANAGEMENT]')
        self.view = SalesViewManager()
        self.sale_operation = SaleManagement()

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

    def get_product(self, product_id: int) -> Product:
        try:
            product = self.sale_operation.get_full_product(product_id)
            self.view.show_message(f"Se agregó {product.product_name} a la lista de venta.")
            controller_logger.info(f'"{product.product_name}" added to cart.')
            return product
        
        except ProductNotFoundError:
            self.view.show_message("Producto no encontrado.")
        except Exception as e:
            self.view.show_message(f"Error inesperado: {e}")
    
    def ask_for_remove_product(self) -> str:
        self.view.show_message("Se terminó de agregar productos.")
        cancel_choice = self.view.cancel_product_question()

        return cancel_choice
    
    def remove_product(self, product: Product):
        """
        Handles the process of removing a product from the cart if the user decides not to buy it.
        """
        id_to_cancel = self.view.choice_product_for_cancel()
        controller_logger.info(f'User choice to remove product with ID: {id_to_cancel} from cart.')
        self.sale_operation.cancel_product(id_to_cancel, product)
        self.view.show_message("Producto anulado.")

    def ask_for_continue(self) -> str:
        continue_choice = self.view.continue_with_sale()
        return continue_choice
    
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

    def manage_sale_process(self): 
        # TODO: Refactor this function when the graphical interface is implemented.  
        # If any issue arises, comment out lines 15 and 24 in sales_dao.py where  
        # the exception "raise ProductNotFoundError" is raised, so it is not handled.  

        extern = True
        while extern:
            barcode = self.get_barcode()

            if barcode.lower() == 'c':
                cancel_choice = self.ask_for_remove_product()

                if cancel_choice.lower() == 's':
                    intern = True
                    while intern:
                        self.remove_product(product)
                        continue_choice = self.ask_for_continue()

                        if continue_choice == 1:
                            intern = False
                            extern = False
                        elif continue_choice == 2:
                            continue

                elif cancel_choice.lower() == 'n':
                    extern = False

            else:
                product_id = self.get_id(barcode)
                product = self.get_product(product_id)

        self.update_product_status(product)
        self.choose_pay_method()

        try:
            self.complete_sale()

        except ProductNotFoundError as e:
            self.view.show_message("Un producto a actualizar el stock no fue encontrado.")
        except TransactionIntegrityError as e:
            self.view.show_message("Ocurrió un error al ingresar la venta, inténtelo de nuevo.")
        except Exception as e:
            self.view.show_message(f"Error inesperado: {e}")

