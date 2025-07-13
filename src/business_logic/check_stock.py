from src.data_access import connection
from src.data_access.session_manager import session_scope
from src.data_access.repositories.stock import StockDAO
from src.utils.logger_config import business_logger


class CheckStock:
    def __init__(self):
        self.connection = connection

        business_logger.info('Program flow started. [CHECKING STOCK]')

    def search_product(self, barcode: str):
        with session_scope(self.connection) as session:
            query = StockDAO(session)
            product_name, available_quantity = query.select_name_quantity(barcode)
            business_logger.info(f'Product "{product_name}" Existences: {available_quantity}. [IMPORTANT] CHECKING STOCK PROCESS SUCCESSFULLY ENDED.\n-')
            return product_name, available_quantity