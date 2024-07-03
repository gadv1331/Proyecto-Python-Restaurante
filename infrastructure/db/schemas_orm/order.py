from sqlalchemy import Column, Integer, ForeignKey, String, Table, Float, DateTime
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base
from infrastructure.db.schemas_orm.menu import Menu

order_menu_association = Table(
    'order_menu_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.ord_id')),
    Column('menus_id', Integer, ForeignKey('menus.men_id'))
)

class Order(Base):
    __tablename__ = "orders"
    ord_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ord_quantity = Column(Float)
    ord_price = Column(Float)
    ord_date = Column(DateTime)
    ord_status = Column(String)
    menu_list= relationship("Menu", secondary = order_menu_association, back_populates="orders")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="orders")