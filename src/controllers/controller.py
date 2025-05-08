import flet as ft
from src.controllers.check_stock_controller import StockManagementController
from src.controllers.price_management_controller import PricesManagementController
from src.controllers.sales_management_controller import SalesManagementController
from src.database import connection
from src.utils.logging_config import controller_logger
from src.views.general_views import GeneralViewsManager


class MainController:
    def __init__(self, page):
        self.page = page

        self.ui = GeneralViewsManager(page)

        try: # TODO: Make a snackbar "Connected to database" or something.
            connection.connect()
        except:
            raise Exception

        self.ui.set_callbacks((
            lambda:SalesManagementController(page, self.ui.content),
            lambda:StockManagementController(page, self.ui.content),
            lambda:PricesManagementController(page, self.ui.content),
        ))

        self.ui.change_view(0)
