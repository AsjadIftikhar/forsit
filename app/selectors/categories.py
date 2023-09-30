from sqlalchemy.orm import Session

from app.database.models import Category


def selector_get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def selector_get_category(db: Session, category_id: int):
    """
    Retrieve a category by its ID.

    :param db: Database session
    :param category_id: ID of the category to retrieve
    :return: Category model if found, None if not found
    """
    return db.query(Category).filter(Category.id == category_id).first()
