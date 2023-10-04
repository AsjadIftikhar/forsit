from sqlalchemy.orm import Session, joinedload
from app.database.models import Sale, Product
from typing import Optional
from sqlalchemy import func
from enum import Enum
from datetime import datetime, timedelta
from fastapi import HTTPException


class TimeIntervals(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


def selector_compare_revenue_by_date_range(db: Session, start_date1: datetime, end_date1: datetime,
                                           start_date2: datetime, end_date2: datetime):
    total_revenue1 = db.query(func.sum(Sale.revenue)).filter(
        Sale.sale_date >= start_date1,
        Sale.sale_date <= end_date1
    ).scalar()

    total_revenue2 = db.query(func.sum(Sale.revenue)).filter(
        Sale.sale_date >= start_date2,
        Sale.sale_date <= end_date2
    ).scalar()

    return {
        "revenue_range_1": total_revenue1 or 0.0,
        "revenue_range_2": total_revenue2 or 0.0,
    }


def selector_compare_revenue_by_categories(db: Session, category_id1: int, category_id2: int):
    total_revenue1 = db.query(func.sum(Sale.revenue)).join(Sale.product).filter(
        Product.category_id == category_id1
    ).scalar()

    total_revenue2 = db.query(func.sum(Sale.revenue)).join(Sale.product).filter(
        Product.category_id == category_id2
    ).scalar()

    return {
        "revenue_category_1": total_revenue1 or 0.0,
        "revenue_category_2": total_revenue2 or 0.0,
    }


def selector_calculate_revenue_by_interval(db: Session, interval: TimeIntervals):
    today = datetime.utcnow()
    start_date = None
    end_date = today

    if interval == TimeIntervals.daily:
        start_date = today - timedelta(days=1)
    elif interval == TimeIntervals.weekly:
        start_date = today - timedelta(weeks=1)
    elif interval == TimeIntervals.monthly:
        start_date = today - timedelta(days=30)  # Approximate for a month
    elif interval == TimeIntervals.yearly:
        start_date = today - timedelta(days=365)  # Approximate for a year

    if not start_date:
        raise HTTPException(status_code=400, detail="Invalid interval")

    # Query the database to calculate revenue within the specified interval
    total_revenue = db.query(func.sum(Sale.revenue)).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).scalar()

    return total_revenue or 0.0


def selector_get_sales_by_filters(
        db: Session,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10
):
    query = db.query(Sale).options(
        joinedload(Sale.product).joinedload(Product.category)
    )

    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if start_date and end_date:
        query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    return query.offset(skip).limit(limit).all()
