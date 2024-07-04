from sqlalchemy import Column, Integer, ForeignKey, String, Table, Float, DateTime
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base

order_dish_association = Table(
    'order_dish_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.ord_id')),
    Column('dish_id', Integer, ForeignKey('dish.dis_id'))
)

class Order(Base):
    __tablename__ = "orders"
    ord_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ord_quantity = Column(Float)
    ord_price = Column(Float)
    ord_date = Column(DateTime)
    ord_status = Column(String)
    dish_list = relationship("Dish", secondary=order_dish_association, back_populates="orders")
    user_id = Column(Integer, ForeignKey('users.id'))