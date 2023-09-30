from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.selectors.categories import selector_get_categories, selector_get_category
from app.services.categories import service_create_category, service_delete_category, service_update_category
from app.serializers.categories import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = selector_get_categories(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return service_create_category(db, category)


@router.put("/{category_id}", response_model=CategoryUpdate)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    category = selector_get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    updated_category = service_update_category(db, category, category_update)
    return updated_category


@router.delete("/{category_id}", response_model=None)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = selector_get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    service_delete_category(db, category)
    return Response(status_code=204)
