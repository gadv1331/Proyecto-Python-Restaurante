from infrastructure.db.repositories.order_repository import OrderRepository
from domain.schemas.order import Order, OrderCreate, OrderUpdate
from typing import List, Optional

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, order_data: OrderCreate) -> Order:
        return self.order_repository.create_order(order_data)

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        db_order = self.order_repository.get_order(order_id)
        if db_order:
            return self.order_repository.update_order(db_order, order_data)
        return None

    def delete_order(self, order_id: int) -> Optional[Order]:
        db_order = self.order_repository.get_order(order_id)
        if db_order:
            return self.order_repository.delete_order(db_order)
        return None

    def get_order(self, order_id: int) -> Optional[Order]:
        db_order = self.order_repository.get_order(order_id)
        if db_order:
            return Order.from_orm(db_order)
        return None

    def get_all_orders(self) -> List[Order]:
        db_orders = self.order_repository.get_all_orders()
        return [Order.from_orm(order) for order in db_orders]