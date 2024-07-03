from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.schemas.menu import Menu
from domain.schemas.user import User

class OrderCreate(BaseModel):
    ord_quantity: float
    ord_price: float
    ord_date: datetime
    menu_list: List[Menu] = []
    user: User

class OrderUpdate(BaseModel):
    ord_quantity: float
    ord_price: float
    menu_list: List[Menu] = []
    user: User

class Order(BaseModel):
    ord_id: int
    ord_quantity: float
    ord_price: float
    ord_date: datetime
    ord_status: str
    menu_list: List[Menu] = []
    user: User

    class Config:
        from_orm = True
        from_attributes = True