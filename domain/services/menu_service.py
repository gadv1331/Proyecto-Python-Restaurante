from infrastructure.db.repositories.menu_repository import MenuRepository
from domain.schemas.menu import Menu, MenuCreate
from typing import List, Optional

class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def create_menu(self, menu_data: MenuCreate) -> Menu:
        return self.menu_repository.create_menu(menu_data)
    
    def add_dish_to_menu(self, menu_id: int, dish_id: int) -> Optional[Menu]:
        return self.menu_repository.add_dish_to_menu(menu_id, dish_id)
    
    def remove_dish_from_menu(self, menu_id: int, dish_id: int) -> Optional[Menu]:
        return self.menu_repository.remove_dish_from_menu(menu_id, dish_id)
    
    def get_menu(self, menu_id: int) -> Optional[Menu]:
        db_menu = self.menu_repository.get_menu(menu_id)
        if db_menu:
            return Menu.from_orm(db_menu)
        return None
    
    def get_all_menus(self) -> List[Menu]:
        db_menus = self.menu_repository.get_all_menus()
        return [Menu.from_orm(menu) for menu in db_menus]
    