from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                               QPushButton, QStackedWidget, QVBoxLayout,
                               QWidget)

from src.controllers.check_stock import StockManagementController
from src.controllers.manage_prices import PricesManagementController
from src.controllers.register_sale import SalesManagementController
from src.controllers.settings import SettingsController
from src.data_access import connection
from src.utils.logger_config import controller_logger
from src.views.check_stock import CheckStockViewManager
from src.views.main_views import GeneralViewsManager
from src.views.manage_prices import PriceViewManager
from src.views.register_sale import SalesViewManager
from src.views.settings import SettingsViewManager


class MainController:
    def __init__(self):
        # Domain controllers
        self.stock_controller = StockManagementController()
        self.price_controller = PricesManagementController()
        self.sales_controller = SalesManagementController()
        self.settings_controller = SettingsController()

        self.check_stock_view = CheckStockViewManager(self.stock_controller)
        self.price_view = PriceViewManager(self.price_controller)
        self.sales_view = SalesViewManager(self.sales_controller)
        self.settings_view = SettingsViewManager(self.settings_controller)

        self.ui = GeneralViewsManager(
            self,
            self.check_stock_view,
            self.price_view,
            self.sales_view,
            self.settings_view
        )

        self.stock_controller.view = self.check_stock_view
        self.price_controller.view = self.price_view
        self.sales_controller.view = self.sales_view
        self.settings_controller = self.settings_view
    
    def quit_app(self) -> None:
        QApplication.quit()

