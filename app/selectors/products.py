from sqlalchemy.orm import Session

from app.database.models import Product

from sqlalchemy.orm import joinedload


def selector_get_products(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of products with pagination.

    :param db: Database session
    :param skip: Number of records to skip (for pagination)
    :param limit: Maximum number of records to return (for pagination)
    :return: List of Product models
    """
    return (
        db.query(Product)
        .filter(Product.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .options(joinedload(Product.category))
        .all()
    )


def selector_get_product(db: Session, product_id: int):
    """
    Retrieve a product by its ID.

    :param db: Database session
    :param product_id: ID of the product to retrieve
    :return: Product model if found, None if not found
    """
    return (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .options(joinedload(Product.category))
        .first()
    )
