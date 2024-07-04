from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.schemas.dish import Dish
from domain.schemas.user import User

class OrderCreate(BaseModel):
    ord_quantity: float
    ord_price: float
    ord_user_id: int
    dish_list: List[Dish] = []

class OrderUpdate(BaseModel):
    ord_quantity: float
    ord_price: float
    ord_status: str
    dish_list: List[Dish] = []
    ord_user_id: int

class Order(BaseModel):
    ord_id: int
    ord_quantity: float
    ord_price: float
    ord_date: datetime
    ord_status: str
    dish_list: List[Dish] = []
    ord_user_id: int

    class Config:
        from_orm = True
        from_attributes = True