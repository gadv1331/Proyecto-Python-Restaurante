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
    
    def delete_dish(self, dish_id: int):
        return self.dish_repository.delete_dish(dish_id)
    
    def get_dish(self, dish_id: int) -> Optional[Dish]:
        db_dish = self.dish_repository.get_dish_by_id(dish_id)
        if db_dish:
            return db_dish
        return None
    
    def get_all_dishes(self) -> List[Dish]:
        db_dishes = self.dish_repository.get_all_dishes()
        return [dish for dish in db_dishes]
    
    def add_recipe_to_dish(self, dish_id: int, recipe_data: RecipeCreate) -> Optional[Recipe]:
        return self.dish_repository.add_recipe_to_dish(dish_id, recipe_data)
    
    def remove_recipe_from_dish(self, dish_id: int, recipe_id: int) -> Optional[Recipe]:
        return self.dish_repository.remove_recipe_from_dish(dish_id, recipe_id)
    
    def update_recipe_in_dish(self, dish_id: int, recipe_id: int, recipe_data: RecipeCreate) -> Optional[Recipe]:
        return self.dish_repository.update_recipe_in_dish(dish_id, recipe_id, recipe_data)
    
    def get_recipes_of_dish(self, dish_id: int) -> List[Recipe]:
        db_recipes = self.dish_repository.get_recipes_of_dish(dish_id)
        return [recipe for recipe in db_recipes]
    

    


    
