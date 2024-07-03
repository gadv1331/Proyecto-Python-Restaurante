from pydantic import BaseModel
from typing import List
from domain.schemas.dish import Dish

class MenuCreate(BaseModel):
    men_name: str

class Menu(BaseModel):
    men_id: int
    men_name: str
    dish_list: List[Dish] = []

    class Config:
        from_attributes = True
        from_orm = True