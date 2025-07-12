from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.data_access.database_tables import Sales, Stock
from src.exceptions import (DBError, ProductNotFoundError,
                            TransactionIntegrityError)
from src.utils.logging_config import data_access_logger


class SalesDAO:
    def __init__(self, session):
        self.session = session

    def insert_sale_record(self, total_quantity, amount, pay_method, sale_date, sale_hour):
        try:
            sale = Sales(db_purchased_quantity=total_quantity, db_amount=amount, db_payment_method=pay_method, db_date=sale_date, db_hour=sale_hour)
            self.session.add(sale)
            self.session.flush()
            return sale.id
        
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (INSERT). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(INSERT). Exception details: {e}')
            raise DBError(original_exception=e)