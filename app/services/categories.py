from sqlalchemy.orm import Session
from app.database.models import Category
from app.serializers.categories import CategoryCreate, CategoryUpdate


def service_create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def service_update_category(db: Session, category: Category, category_update: CategoryUpdate):
    """
    Update a category's information in the database.

    :param db: Database session
    :param category: Category model to update
    :param category_update: Updated category information
    :return: Updated category
    """
    for key, value in category_update.dict().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def service_delete_category(db: Session, category: Category):
    """
    Delete a category from the database.

    :param db: Database session
    :param category: Category model to delete
    :return: Deleted category
    """
    db.delete(category)
    db.commit()
    return category
