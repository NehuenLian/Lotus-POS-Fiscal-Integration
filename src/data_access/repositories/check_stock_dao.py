from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from src.data_access.database_tables import Sales, SalesDetails, Stock
from src.exceptions import DBError, ProductNotFoundError
from src.utils.logger import console_logger, data_access_logger


class CheckStockDAO:
    def __init__(self, session):
        self.session = session

    def select_name_quantity(self, barcode: str) -> Tuple[int, str, str, int]: # check_stock.py
        try:
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.id, product.db_barcode, product.db_product_name, product.db_available_quantity
        
        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for barcode "{barcode}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)