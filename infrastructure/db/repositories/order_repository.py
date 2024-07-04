from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from infrastructure.db.schemas_orm.order import Order as OrderModel
from infrastructure.db.schemas_orm.dish import Dish as DishModel
from infrastructure.db.schemas_orm.user import User as UserModel
from domain.schemas.order import OrderCreate, OrderUpdate, Order
from datetime import datetime
from fastapi.responses import JSONResponse

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: OrderCreate) -> Order:
        try:
            db_order = OrderModel(
                ord_quantity=order_data.ord_quantity,
                ord_price=order_data.ord_price,
                ord_date=datetime.now(),
                ord_status="Pendiente",
                ord_user_id=order_data.ord_user_id
            )
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)

            db_order.dish_list = self.db.query(DishModel).filter(DishModel.dis_id.in_(order_data.dish_list)).all()
            self.db.commit()
            self.db.refresh(db_order)

            return Order.from_orm(db_order)
        except IntegrityError as e:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado."})

    def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        db_order = self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()
        if db_order:
            db_order.ord_quantity = order_data.ord_quantity
            db_order.ord_price = order_data.ord_price
            db_order.ord_status = order_data.ord_status
            db_order.dish_list = self.db.query(DishModel).filter(DishModel.dis_id.in_([dish.dis_id for dish in order_data.dish_list])).all()
            db_order.ord_user_id = order_data.ord_user_id
            self.db.commit()
            self.db.refresh(db_order)
            return Order.from_orm(db_order)
        return None

    def get_order(self, order_id: int) -> Optional[Order]:
        db_order = self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()
        if db_order:
            return Order.from_orm(db_order)
        return None

    def get_orders_by_user(self, user_id: int) -> List[Order]:
        db_orders = self.db.query(OrderModel).filter(OrderModel.ord_user_id == user_id).all()
        return [Order.from_orm(order) for order in db_orders]

    def get_orders_by_dish(self, dish_id: int) -> List[Order]:
        db_orders = self.db.query(OrderModel).join(OrderModel.dish_list).filter(DishModel.dis_id == dish_id).all()
        return [Order.from_orm(order) for order in db_orders]

    def get_all_orders(self) -> List[Order]:
        db_orders = self.db.query(OrderModel).all()
        return [Order.from_orm(order) for order in db_orders]
    
    def add_dish_to_order(self, order_id: int, dish_id: int) -> Order:
        db_order = self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()
        if db_order:
            db_dish = self.db.query(DishModel).filter(DishModel.dis_id == dish_id).first()
            if db_dish:
                db_order.ord_price = db_order.ord_price + db_dish.dis_price_by_unit
                db_order.dish_list.append(db_dish)
                self.db.commit()
                self.db.refresh(db_order)
                return Order.from_orm(db_order)
            else:
                return None
        return None

    def delete_order(self, order_id: int) -> None:
        db_order = self.db.query(OrderModel).filter(OrderModel.ord_id == order_id).first()
        if db_order:
            try:
                self.db.delete(db_order)
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                return None