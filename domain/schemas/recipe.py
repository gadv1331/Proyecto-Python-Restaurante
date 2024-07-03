from pydantic import BaseModel

class RecipeCreate(BaseModel):
    rec_quantity: int
    #ing_id_fk: int

class Recipe(BaseModel):
    rec_id: int
    rec_quantity: int
    #ing_id_fk: int

    class Config:
        from_orm = True
        from_attributes = True



