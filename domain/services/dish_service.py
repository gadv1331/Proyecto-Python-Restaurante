from infrastructure.db.repositories.dish_repository import DishRepository
from domain.schemas.dish import DishCreate, Dish
from domain.schemas.recipe import RecipeCreate, Recipe
from typing import List, Optional

class DishService:
    def __init__(self, dish_repository: DishRepository):
        self.dish_repository = dish_repository

    def create_dish(self, dish: DishCreate):
        return self.dish_repository.create_dish(dish)
    
    def update_dish(self, dish_id: int, dish_data: DishCreate):
        return self.dish_repository.update_dish(dish_id, dish_data)
    
    def delete_dish(self, dish_id: int) -> Optional[Dish]:
        deleted_dish = self.dish_repository.delete_dish(dish_id)
        return deleted_dish
    
    def get_dish(self, dish_id: int) -> Optional[Dish]:
        db_dish = self.dish_repository.get_dish_by_id(dish_id)
        if db_dish:
            return db_dish
        return None
    
    def get_all_dishes(self) -> List[Dish]:
        return self.dish_repository.get_all_dishes()
    
    def add_recipe_to_dish(self, dish_id: int, ingredient_id: int, quantity: int) -> Optional[Recipe]:
        added_recipe = self.dish_repository.add_recipe_to_dish(dish_id, ingredient_id, quantity)
        return added_recipe
    
    def remove_recipe_from_dish(self, dish_id: int, recipe_id: int) -> Optional[Recipe]:
        removed_recipe = self.dish_repository.remove_recipe_from_dish(dish_id, recipe_id)
        return removed_recipe
    
    def update_recipe_of_dish(self, dish_id: int, recipe_id: int, recipe_data: RecipeCreate) -> Optional[Recipe]:
        updated_recipe = self.dish_repository.update_recipe_of_dish(dish_id, recipe_id, recipe_data)
        return updated_recipe
    
    def get_recipes_of_dish(self, dish_id: int) -> List[Recipe]:
        return self.dish_repository.get_recipes_of_dish(dish_id)
    

    


    
