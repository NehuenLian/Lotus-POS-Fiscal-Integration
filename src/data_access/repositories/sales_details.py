from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.data_access.database_tables import SalesDetails
from src.exceptions import DBError, TransactionIntegrityError
from src.utils.logger_config import data_access_logger


class SalesDetailsDAO:
    def __init__(self, session):
        self.session = session

    def insert_sale_detail(self, sale_id, product_id, quantity, unit_price, subtotal):
        try:
            detail = SalesDetails(db_sale_id=sale_id, db_product_id=product_id, db_quantity=quantity, db_unit_price=unit_price, db_subtotal=subtotal)
            self.session.add(detail)
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (INSERT). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(INSERT). Exception details: {e}')
            raise DBError(original_exception=e)
