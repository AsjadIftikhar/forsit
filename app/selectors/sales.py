from sqlalchemy.orm import Session
from app.database.models import Sale, Product
from datetime import datetime
from typing import Optional


def selector_get_sales_by_filters(
        db: Session,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10
):
    """
    Retrieve a list of sales based on provided filters with pagination.

    :param db: Database session
    :param product_id: ID of the product to filter by (optional)
    :param category_id: ID of the category to filter by (optional)
    :param start_date: Start date of the sale date range (optional)
    :param end_date: End date of the sale date range (optional)
    :param skip: Number of records to skip (for pagination)
    :param limit: Maximum number of records to return (for pagination)
    :return: List of Sale models based on the provided filters
    """
    query = db.query(Sale)

    # Apply product_id filtering if provided
    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    # Apply category_id filtering if provided
    if category_id is not None:
        query = query.join(Sale.product).filter(Product.category_id == category_id)

    # Apply date range filtering if start_date and end_date are provided
    if start_date and end_date:
        query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    return query.offset(skip).limit(limit).all()
