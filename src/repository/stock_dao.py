from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from src.database.models import Stock
from src.exceptions import (DBError, ProductNotFoundError,
                            TransactionIntegrityError)
from src.utils.logging_config import data_access_logger


class StockDAO:
    def __init__(self, session):
        self.session = session

    def select_name_quantity(self, barcode: str): # check_stock.py
        try:
            data_access_logger.warning("Consulting...")
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.db_product_name, product.db_available_quantity
        
        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for barcode "{barcode}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def check_product_exists_by_barcode(self, barcode: str): # sales_management.py
        try:
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.id
        
        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for barcode "{barcode}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def get_product(self, product_id: int): # sales_management.py
        try:
            product = self.session.execute(select(Stock).filter_by(id=product_id)).scalar_one()
            return product.id, product.db_barcode, product.db_product_name, product.db_available_quantity, product.db_final_price_to_consumer
        
        except NoResultFound as e:
            raise ProductNotFoundError(barcode_or_id=product_id, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def update_stock_table(self, product_id, quantity_purchased): # sales_management.py
        try:
            product_to_update = self.session.execute(select(Stock).filter_by(id=product_id)).scalar_one()
            new_quantity = product_to_update.db_available_quantity - quantity_purchased
            product_to_update.db_available_quantity = new_quantity

        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for ID "{product_id}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=product_id, original_exception=e)
        
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (UPDATE). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(FULL TRANSACTION:SELECT, UPDATE). Exception details: {e}')
            raise DBError(original_exception=e)

    def select_id_name_price(self, barcode: str): # price_management.py
        try:
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.id, product.db_product_name, product.db_final_price_to_consumer
        
        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for barcode "{barcode}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def update_price_in_db(self, product_id: int, new_price: float): # price_management.py
        try:
            self.session.query(Stock).filter(Stock.id == product_id).update({"db_final_price_to_consumer": new_price})
        
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (UPDATE). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(UPDATE). Exception details: {e}')
            raise DBError(original_exception=e)
