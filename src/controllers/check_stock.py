from src.business_logic.check_stock import CheckStock
from src.exceptions import ProductNotFoundError


class StockManagementController:
    def __init__(self):
        self._view = None
        self.check_stock = CheckStock()

    @property
    def view(self):
        return self._view
    
    @view.setter
    def view(self, view):
        self._view = view

    def check_product_existence(self, barcode):
        try:
            product_name, available_quantity = self.check_stock.search_product(barcode)
            print(product_name, available_quantity)
            #self.view.display_product(product_name, available_quantity)

        except ProductNotFoundError as e:
            print("Producto no encontrado.")

        except Exception as e:
            print(f"Error inesperado: {e}")