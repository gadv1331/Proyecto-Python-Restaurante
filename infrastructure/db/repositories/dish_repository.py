from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.dish import Dish as DishModel
from infrastructure.db.schemas_orm.recipe import Recipe as RecipeModel
from domain.schemas.dish import DishCreate

class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_dish_by_id(self, dish_id: int) -> DishModel:
        return self.db.query(DishModel).filter(DishModel.id == dish_id).first()
    
    def get_all_dishes(self) -> list[DishModel]:
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
        
    def delete_dish(self, dish_id: int):
        db_dish = self.get_dish_by_id(dish_id)
        if(db_dish):
            self.db.delete(db_dish)
            self.db.commit()
            return True
        return False

    def add_recipe_to_dish(self, dish_id: int, recipe_data):
        db_dish = self.get_dish_by_id(dish_id)
        if(db_dish):
            db_recipe = RecipeModel(**recipe_data.dict(), dis_id_fk = dish_id)
            self.db.add(db_recipe)
            self.db.commit()
            self.db.refresh(db_dish)
            return db_recipe
        return None

    def remove_recipe_from_dish(self, dish_id: int, recipe_id: int):
        db_dish = self.get_dish_by_id(dish_id)
        if db_dish:
            db_recipe = self.db.query(RecipeModel).filter(RecipeModel.id == recipe_id, RecipeModel.dis_id_fk == dish_id).first()
            if db_recipe:
                self.db.delete(db_recipe)
                self.db.commit()
                return True
            return False
    
    def update_recipe_of_dish(self, dish_id: int, recipe_id: int, recipe_data):
        db_dish = self.get_dish_by_id(dish_id)
        if db_dish:
            db_recipe = self.db.query(RecipeModel).filter(RecipeModel.id == recipe_id, RecipeModel.dis_id_fk == dish_id).first()
            if db_recipe:
                for key, value in recipe_data.dict(exclude_unset = True).items():
                    setattr(db_recipe, key, value)
                self.db.commit()
                self.db.refresh(db_recipe)
                return db_recipe
        return None
    
    def get_recipe_of_dish(self, dish_id: int) -> List[RecipeModel]:
        db_dish = self.get_dish_by_id(dish_id)
        if db_dish:
            return self.db.query(RecipeModel).filter(RecipeModel.dis_id_fk == dish_id).all()
        return []
    
    
    