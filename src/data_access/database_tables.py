from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Time
from sqlalchemy.orm import DeclarativeBase, relationship

from src.data_access import connection


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = 'inventory_stock'

    id = Column(Integer, primary_key=True, nullable=False)
    db_barcode = Column(String(100), unique=True, nullable=True)
    db_product_name = Column(String(100))
    db_available_quantity = Column(Integer, nullable=True)
    db_price_excluding_tax = Column(Numeric(7, 2), nullable=True)
    db_price_including_tax = Column(Numeric(7, 2), nullable=True)
    db_final_price_to_consumer = Column(Numeric(7, 2), nullable=False)

    sales_details = relationship("SalesDetails", back_populates="product")


class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, nullable=False)
    db_purchased_quantity = Column(Integer, nullable=False)
    db_amount = Column(Numeric(7, 2), nullable=False)
    db_payment_method = Column(String(100), nullable=False)
    db_date = Column(Date, nullable=False)
    db_hour = Column(Time, nullable=False)

    details = relationship("SalesDetails", back_populates="sale")


class SalesDetails(Base):
    __tablename__ = 'sales_details'

    db_detail_id = Column(Integer, primary_key=True, nullable=False)
    db_sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    db_product_id = Column(Integer, ForeignKey('inventory_stock.id'), nullable=False)
    db_quantity = Column(Integer, nullable=False)
    db_unit_price = Column(Numeric(7, 2), nullable=False)
    db_subtotal = Column(Numeric(7, 2), nullable=False)

    sale = relationship("Sales", back_populates="details")
    product = relationship("Stock", back_populates="sales_details")


Base.metadata.create_all(connection.engine)
