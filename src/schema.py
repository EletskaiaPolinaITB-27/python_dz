from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: float
    is_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    is_available: bool | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)