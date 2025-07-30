import datetime
from decimal import Decimal  # Only for typing
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.data_access.database_tables import Sales, SalesDetails, Stock
from src.exceptions import (DBError, ProductNotFoundError,
                            TransactionIntegrityError)
from src.utils.logger import console_logger, data_access_logger


class RegisterSaleDAO:
    def __init__(self, session):
        self.session = session

    def get_product(self, barcode: str) -> Tuple[int, str, str, int, Decimal, Decimal, Decimal]:
        try:
            product = self.session.execute(select(Stock).filter_by(db_barcode=barcode)).scalar_one()
            return product.id, product.db_barcode, product.db_product_name, product.db_available_quantity, product.db_price_excl_vat, product.db_price_incl_vat, product.db_final_price_to_consumer
        
        except NoResultFound as e:
            raise ProductNotFoundError(barcode_or_id=barcode, original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(SELECT). Exception details: {e}')
            raise DBError(original_exception=e)

    def update_stock_table(self, product_id: int, quantity_purchased: int) -> None:
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
        
    def insert_sale_record(self, total_quantity: int, amount: Decimal, amount_excl_vat: Decimal, amount_only_vat: Decimal, pay_method: str, sale_date: datetime.date, sale_hour: datetime.time) -> int:
        try:
            sale = Sales(db_purchased_quantity=total_quantity, 
                        db_amount=amount,
                        db_net_amount=amount_excl_vat,
                        db_total_iva_amount=amount_only_vat,
                        db_payment_method=pay_method, 
                        db_date=sale_date, 
                        db_hour=sale_hour,
                        db_is_invoiced=False,
                    )
            self.session.add(sale)
            self.session.flush()
            return sale.id
        
        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (INSERT). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(INSERT). Exception details: {e}')
            raise DBError(original_exception=e)
        
    def insert_sale_detail(self, sale_id: int, product_id: int, quantity: int, unit_price: Decimal, subtotal: Decimal) -> None:
        try:
            detail = SalesDetails(db_sale_id=sale_id, 
                                db_product_id=product_id, 
                                db_quantity=quantity, 
                                db_unit_price=unit_price, 
                                db_subtotal=subtotal
                            )
            self.session.add(detail)

        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (INSERT). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(INSERT). Exception details: {e}')
            raise DBError(original_exception=e)
        
    def update_sale_fiscal_status(self, sale_id: int, status: bool):
        try:
            sale_to_update = self.session.execute(select(Sales).filter_by(id=sale_id)).scalar_one()
            sale_to_update.db_is_invoiced = status
            self.session.commit()

        except NoResultFound as e:
            data_access_logger.warning(f'No result found in database for ID "{sale_id}". Exception details: {e}')
            raise ProductNotFoundError(barcode_or_id=sale_id, original_exception=e)

        except IntegrityError as e:
            data_access_logger.exception(f'Database integrity constraint violated during data access operation (UPDATE). Exception details: {e}')
            raise TransactionIntegrityError(original_exception=e)
        
        except SQLAlchemyError as e:
            data_access_logger.exception(f'Unexpected database error during data access operation(FULL TRANSACTION:SELECT, UPDATE). Exception details: {e}')
            raise DBError(original_exception=e)