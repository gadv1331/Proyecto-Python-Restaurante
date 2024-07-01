from pydantic import BaseModel

class DishCreate(BaseModel):
    dis_name: str
    dis_description: str
    dis_price_by_unit: float

class Dish(BaseModel):
    dis_id: int
    dis_name: str
    dis_description: str
    dis_price_by_unit: float

    class Config:
        orm_mode = True