from decimal import Decimal  # Only for typing
from typing import Tuple

from src.data_access.repositories.manage_prices_dao import ManagePricesDAO
from src.data_access.session_manager import session_scope
from src.exceptions import InvalidPriceError
from src.utils.logger_config import business_logger


class PriceManagement:
    def __init__(self):
        pass

    def search_product(self, barcode: str) -> Tuple[int, str, str, Decimal]:
        with session_scope() as session:
            query = ManagePricesDAO(session)
            id, barcode, product_name, price = query.select_id_name_price(barcode)
            business_logger.info(f'Product found: "{product_name}" (ID: {id}) at ${price}')

            return id, barcode, product_name, price

    def update_prices(self, id: int, new_price: float):

        if not self._is_price_valid(new_price):
            business_logger.warning(f"Invalid price: {new_price}")
            raise InvalidPriceError

        with session_scope() as session:
            query = ManagePricesDAO(session)
            query.update_price_in_db(id, new_price)
            business_logger.info(f'Updated price for Product (ID {id}): ${new_price}')
            business_logger.info('[IMPORTANT] PRICE SUCCESSFULLY UPDATED. PROCESS ENDED SUCCESSFULL.\n-')

    # Validations
    def _is_price_valid (self, new_price: float) -> bool:
        if isinstance(new_price, float) and new_price >= 1:
            return True
        else:
            return False