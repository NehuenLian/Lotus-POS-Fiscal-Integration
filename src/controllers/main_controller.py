from src.controllers.check_stock import StockManagementController
from src.controllers.manage_prices import \
    PricesManagementController
from src.controllers.register_sale import \
    SalesManagementController
from src.data_access import connection
from src.utils.logger_config import controller_logger
from src.views.main_views import GeneralViewsManager

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QHBoxLayout, QStackedWidget, QFrame
)


class MainController:
    def __init__(self):
        self.ui = GeneralViewsManager(self)

    def check_stock(self):
        stock_controller = StockManagementController()
        stock_controller.manage_check_stock()
        
    def manage_prices(self):
        prices_controller = PricesManagementController()
        prices_controller.manage_update_prices_process()

    def register_sale(self):
        sales_controller = SalesManagementController()
        sales_controller.manage_sale_process()
    
    def quit_app(self):
        QApplication.quit()

