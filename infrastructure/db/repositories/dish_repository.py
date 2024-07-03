from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.dish import Dish as DishModel
from infrastructure.db.schemas_orm.recipe import Recipe as RecipeModel
from infrastructure.db.schemas_orm.ingredient import Ingredient as IngredientModel
from domain.schemas.dish import DishCreate
from domain.schemas.recipe import RecipeCreate
from typing import List, Optional

class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dish_by_id(self, dish_id: int) -> DishModel:
        return self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
    
    def get_all_dishes(self) -> List[DishModel]:
        return self.db.query(DishModel).all()
    
    def create_dish(self, dish: DishCreate):
        db_dish = DishModel(**dish.dict())
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish
    
    def update_dish(self, dish_id: int, dish_data):
        db_dish = self.get_dish_by_id(dish_id)
        if(db_dish):
            for key, value in dish_data.dict(exclude_unset = True).items():
                setattr(db_dish, key, value)
            self.db.commit()
            self.db.refresh(db_dish)
            return db_dish
        
    def delete_dish(self, dish_id: int) -> Optional[DishModel]:
        db_dish = self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
        if db_dish:
            self.db.delete(db_dish)
            self.db.commit()
            return db_dish
        return None

    def add_recipe_to_dish(self, dish_id: int, ingredient_id: int, quantity: int) -> Optional[RecipeModel]:
        db_dish = self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
        db_ingredient = self.db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
        if db_dish and db_ingredient:
            new_recipe = RecipeModel(
                dis_id_fk=dish_id,
                ing_id_fk=ingredient_id,
                rec_quantity=quantity
            )
            self.db.add(new_recipe)
            self.db.commit()
            self.db.refresh(new_recipe)
            return new_recipe
        return None



    def remove_recipe_from_dish(self, dish_id: int, recipe_id: int) -> Optional[RecipeModel]:
        db_recipe = self.db.query(RecipeModel).filter(RecipeModel.dis_id_fk == dish_id, RecipeModel.rec_id == recipe_id).first()
        if db_recipe:
                self.db.delete(db_recipe)
                self.db.commit()
                return db_recipe
        return None
    
    def update_recipe_of_dish(self, dish_id: int, recipe_id: int, recipe_data: RecipeCreate) -> Optional[RecipeModel]:
        db_recipe = self.db.query(RecipeModel).filter(RecipeModel.dis_id_fk == dish_id, RecipeModel.rec_id == recipe_id).first()
        if db_recipe:
                for key, value in recipe_data.dict().items():
                    setattr(db_recipe, key, value)
                self.db.commit()
                self.db.refresh(db_recipe)
                return db_recipe
        return None
    
    def get_recipes_of_dish(self, dish_id: int) -> List[RecipeModel]:
        db_dish = self.get_dish_by_id(dish_id)
        if db_dish:
            return self.db.query(RecipeModel).filter(RecipeModel.dis_id_fk == dish_id).all()
        return []
    

    