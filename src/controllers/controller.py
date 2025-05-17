from decouple import config

from src.controllers.check_stock_controller import StockManagementController
from src.controllers.price_management_controller import \
    PricesManagementController
from src.controllers.sales_management_controller import \
    SalesManagementController
from src.controllers.settings_controller import SettingsController
from src.database.connection import DataBaseConnection
from src.exceptions import InvalidDatabaseURLError
from src.views.general_views import GeneralViewsManager


class MainController:
    def __init__(self, page):
        self.page = page

        self.ui = GeneralViewsManager(page)

        self.ui.set_callbacks((
            lambda:SalesManagementController(page, self.ui.content),
            lambda:StockManagementController(page, self.ui.content),
            lambda:PricesManagementController(page, self.ui.content),
            lambda:SettingsController(page, self.ui.content)
        ))

        self.ui.change_view(0)
        self._connect_to_db()

    def _connect_to_db(self):
        db_url = config("DATABASE_URL")
        try:
            database = DataBaseConnection(db_url)
            database.connect()
        except InvalidDatabaseURLError:
            pass
