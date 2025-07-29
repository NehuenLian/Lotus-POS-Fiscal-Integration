from decimal import Decimal  # Only for typing
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.data_access.database_tables import Sales, SalesDetails, Stock
from src.exceptions import (DBError, ProductNotFoundError,
                            TransactionIntegrityError)
from src.utils.logger import console_logger, data_access_logger


class ManagePricesDAO:
    def __init__(self, session):
        self.session = session

    def select_id_name_price(self, barcode: str) -> Tuple[int, str, str, Decimal]:
        try:
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.id, product.db_barcode, product.db_product_name, product.db_final_price_to_consumer
        
        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for barcode "{barcode}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def update_price_in_db(self, product_id: int, new_price: float) -> None:
        try:
            self.session.query(Stock).filter(Stock.id == product_id).update({"db_final_price_to_consumer": new_price})
        
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (UPDATE). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(UPDATE). Exception details: {e}')
            raise DBError(original_exception=e)
