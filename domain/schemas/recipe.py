from pydantic import BaseModel

class RecipeCreate(BaseModel):
    quantity: int
    dis_id_fk: int
    ing_id_fk: int

class Recipe(BaseModel):
    rec_id: int
    quantity: int
    dis_id_fk: int
    ing_id_fk: int

    class Config:
        orm_mode = True



