from infrastructure.db.repositories.ingredient_repository import IngredientRepository
from domain.schemas.ingredient import IngredientCreate, Ingredient
from typing import List, Optional

class IngredientService:
    def __init__(self, repository: IngredientRepository)
        self.repository = repository

    def get_all_ingredients(self) -> List[Ingredient]:
        db_ingredients = self.repository.get_all_ingredients()
        return [ingredient for ingredient in db_ingredients]
    
    def get_ingridient_by_id(self, ingredient_id: int) -> Optional[Dish]:
        db_ingredient = self.repository.get_ingredient_by_id(ingredient_id)
        if db_ingredient:
            return db_ingredient
        return None
    
    def create_ingredient(self, ingredient: IngredientCreate):
        return self.repository.create_ingredient(ingredient)
    
    def delete_ingredient(self, ingredient_id:int):
        return self.repository.delete_ingredient(ingredient_id)
    
    def update_ingredient(self, ingredient_id: int, ingredient_data: IngredientCreate):
        return self.repository.update_ingredient(ingredient_id, ingredient_data)
