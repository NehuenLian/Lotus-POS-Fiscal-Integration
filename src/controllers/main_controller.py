from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                               QPushButton, QStackedWidget, QVBoxLayout,
                               QWidget)

from src.controllers.check_stock import StockManagementController
from src.controllers.manage_prices import PricesManagementController
from src.controllers.register_sale import SalesManagementController
from src.data_access import connection
from src.utils.logger_config import controller_logger
from src.views.main_views import GeneralViewsManager
from src.views.check_stock import CheckStockViewManager
from src.views.manage_prices import PriceViewManager
from src.views.register_sale import SalesViewManager


class MainController:
    def __init__(self):
        # Controladores de dominio
        self.stock_controller = StockManagementController()
        self.price_controller = PricesManagementController()
        self.sales_controller = SalesManagementController()

        # Vistas (se les pasa su controlador)
        self.check_stock_view = CheckStockViewManager(self.stock_controller)
        self.price_view = PriceViewManager(self.price_controller)
        self.sales_view = SalesViewManager(self.sales_controller)

        # Vista general (se le pasa las vistas)
        self.ui = GeneralViewsManager(
            self,
            self.check_stock_view,
            self.price_view,
            self.sales_view,
        )

        self.stock_controller.view = self.check_stock_view
        self.price_controller.view = self.price_view
        self.sales_controller.view = self.sales_view

    def check_stock(self):
        self.stock_controller.manage_check_stock()
        
    def manage_prices(self):
        self.price_controller.manage_update_prices_process()

    def register_sale(self):
        self.sales_controller.manage_sale_process()
    
    def quit_app(self):
        QApplication.quit()

