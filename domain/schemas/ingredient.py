from pydantic import BaseModel

class IngredientUpdate(BaseModel):
    name:str
    description:str
    
class IngredientCreate(BaseModel):
    name:str
    description:str
    quantity:float

class Ingredient(BaseModel):
    id: int
    name: str
    description: str
    quantity: float
    class Config:
        orm_mode = True