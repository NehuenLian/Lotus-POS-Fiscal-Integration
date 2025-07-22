from typing import Tuple

from src.data_access.repositories.stock import StockDAO
from src.data_access.session_manager import session_scope
from src.utils.logger_config import business_logger


class CheckStock:
    def __init__(self):
        pass

    def search_product(self, barcode: str) -> Tuple[int, str, str, int]:
        with session_scope() as session:
            query = StockDAO(session)
            product_id, product_barcode, product_name, available_quantity = query.select_name_quantity(barcode)
            business_logger.info(f'Product "{product_name}" Existences: {available_quantity}. [IMPORTANT] CHECKING STOCK PROCESS SUCCESSFULLY ENDED.\n-')

            return product_id, product_barcode, product_name, available_quantity