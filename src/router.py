from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Product
from src.schema import ProductCreate, ProductRead, ProductUpdate


product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@product_router.get("/", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)) -> List[Product]:
    return db.query(Product).all()


@product_router.get("/{id}", response_model=ProductRead)
def get_product(id: int, db: Session = Depends(get_db)) -> Product:
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@product_router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
) -> Product:
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@product_router.put("/{id}", response_model=ProductRead)
def update_product(
    id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
) -> Product:
    existing_product = db.query(Product).filter(Product.id == id).first()

    if existing_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = product.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)
    return existing_product


@product_router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)) -> dict:
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return {"message": "Product has been deleted"}