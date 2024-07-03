from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.ingredient import Ingredient as IngredientModel
from domain.schemas.ingredient import IngredientCreate
from typing import List

class IngredientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_ingredients(self) -> list[IngredientModel]:
        return self.db.query(IngredientModel).all()
    
    def get_ingredient_by_id(self, ingredient_id: int) -> IngredientModel:
        return self.db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    
    def create_ingredient(self, new_ingredient: IngredientCreate):
        db_ing = IngredientModel(**new_ingredient.dict())
        self.db.add(db_ing)
        self.db.commit()
        self.db.refresh(db_ing)
        return db_ing
    
    def delete_ingredient(self, ingredient_id: int):
        db_ing = self.get_ingredient_by_id(ingredient_id)
        if(db_ing):
            self.db.delete(db_ing)
            self.db.commit()
            return True
        return False
    
    def update_ingredient(self, ingredient_id: int, ingredient_data):
        db_ingredient = self.get_ingredient_by_id(ingredient_id)
        if (db_ingredient):
            for key, value in ingredient_data.dict(exclude_unset = True).items():
                setattr(db_ingredient, key, value)
            self.db.commit()
            self.db.refresh(db_ingredient)
            return db_ingredient
