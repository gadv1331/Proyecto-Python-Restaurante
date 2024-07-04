from infrastructure.db.repositories.order_repository import OrderRepository
from domain.schemas.order import Order, OrderCreate, OrderUpdate
from typing import List, Optional

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, order_data: OrderCreate) -> Order:
        return self.order_repository.create_order(order_data)

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        return self.order_repository.update_order(order_id, order_data)

    def delete_order(self, order_id: int) -> Optional[Order]:
        db_order = self.order_repository.get_order(order_id)
        if db_order:
            return self.order_repository.delete_order(db_order)
        return None

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.order_repository.get_order(order_id)

    def get_orders_by_user(self, user_id: int) -> List[Order]:
        return self.order_repository.get_orders_by_user(user_id)

    def get_orders_by_dish(self, dish_id: int) -> List[Order]:
        return self.order_repository.get_orders_by_dish(dish_id)

    def get_all_orders(self) -> List[Order]:
        return self.order_repository.get_all_orders()

    def add_dish_to_order(self, order_id: int, dish_id: int) -> Optional[Order]:
        return self.order_repository.add_dish_to_order(order_id, dish_id)