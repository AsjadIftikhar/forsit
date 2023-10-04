from __future__ import annotations

from sqlalchemy.orm import Session
from app.database.models import Product
from app.serializers.products import ProductCreate, ProductUpdate, ProductUpdateStock


def service_create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def service_update_product(db: Session, product: Product, product_update: ProductUpdate | ProductUpdateStock):
    """
    Update a product's information in the database.

    :param db: Database session
    :param product: Product model to update
    :param product_update: Updated product information
    :return: Updated product
    """
    for key, value in product_update.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def service_delete_product(db: Session, product: Product):
    """
    Delete a product from the database.

    :param db: Database session
    :param product: Product model to delete
    :return: Deleted product
    """
    product.deleted = True
    db.commit()
    return product
