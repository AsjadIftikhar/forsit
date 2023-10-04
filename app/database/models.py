from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float, CheckConstraint('price > 0.0', name='check_price_positive'))
    margin = Column(Float)
    stock = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    sales = relationship("Sale", back_populates="product")
    inventory_tracking = relationship("InventoryTracking", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(DateTime, default=datetime.utcnow, index=True)
    quantity = Column(Integer)
    total = Column(Float)
    revenue = Column(Float)

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sales")


class InventoryTracking(Base):
    __tablename__ = "inventory_tracking"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define a relationship to the Product model
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="inventory_tracking")
