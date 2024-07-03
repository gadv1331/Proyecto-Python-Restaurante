from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base


menu_dish_association = Table(
    'menu_dish_association',
    Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.men_id')),
    Column('dish_id', Integer, ForeignKey('dish.dis_id'))
)

class Menu(Base):
    __tablename__ = "menus"

    men_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    men_name = Column(String, unique = True, index = True)

    dish_list = relationship("Dish", secondary = menu_dish_association, back_populates="menus")