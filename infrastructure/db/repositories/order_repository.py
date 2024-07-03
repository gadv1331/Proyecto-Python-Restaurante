from sqlalchemy.orm import Session
from typing import Optional, List
from infrastructure.db.schemas_orm.order import Order as OrderModel
from infrastructure.db.schemas_orm.menu import Menu as MenuModel
from infrastructure.db.schemas_orm.user import User as UserModel
from domain.schemas.order import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: OrderCreate) -> OrderModel:
        db_order = OrderModel(
            ord_status=order_data.ord_status,
            ord_total=order_data.ord_total,
            menu_id=order_data.menu_id,
            user_id=order_data.user_id
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[OrderModel]:
        db_order = self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()
        if db_order:
            for key, value in order_data.dict(exclude_unset=True).items():
                setattr(db_order, key, value)
            self.db.commit()
            self.db.refresh(db_order)
            return db_order
        return None

    def get_order(self, order_id: int) -> Optional[OrderModel]:
        return self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()

    def get_orders_by_user(self, user_id: int) -> List[OrderModel]:
        return self.db.query(OrderModel).filter(OrderModel.user_id == user_id).all()

    def get_orders_by_menu(self, menu_id: int) -> List[OrderModel]:
        return self.db.query(OrderModel).filter(OrderModel.menu_id == menu_id).all()

    def get_all_orders(self) -> List[OrderModel]:
        return self.db.query(OrderModel).all()