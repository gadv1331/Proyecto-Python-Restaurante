from sqlalchemy.orm import Session
from typing import Optional, List
from infrastructure.db.schemas_orm.menu import Menu as MenuModel
from infrastructure.db.schemas_orm.dish import Dish as DishModel
from domain.schemas.menu import MenuCreate

class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_menu(self, menu_data: MenuCreate) -> MenuModel:
        db_menu = MenuModel(men_name = menu_data.men_name)
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu
    
    def add_dish_to_menu(self, menu_id: int, dish_id: int) -> Optional[MenuModel]:
        db_menu = self.db.query(MenuModel).filter(MenuModel.men_id == menu_id).first()
        db_dish = self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
        if db_menu and db_dish:
            db_menu.dish_list.append(db_dish)
            self.db.commit()
            self.db.refresh(db_menu)
            return db_menu
        return None
    
    def remove_dish_from_menu(self, menu_id: int, dish_id: int) -> Optional[MenuModel]:
        db_menu = self.db.query(MenuModel).filter(MenuModel.men_id == menu_id).first()
        db_dish = self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
        if db_menu and db_dish:
            db_menu.dish_list.remove(db_dish)
            self.db.commit()
            self.db.refresh(db_menu)
            return db_menu
        return None

    def get_menu(self, menu_id: int) -> Optional[MenuModel]:
        return self.db.query(MenuModel).filter(MenuModel.men_id == menu_id).first()
    
    def get_all_menus(self) -> List[MenuModel]:
        return self.db.query(MenuModel).all()