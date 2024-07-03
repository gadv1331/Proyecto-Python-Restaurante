from sqlalchemy import Enum, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base
from infrastructure.db.schemas_orm.menu import menu_dish_association


class Dish(Base):
    __tablename__ = "dish"

    dis_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dis_name = Column(String, unique=True, index=True)
    dis_description = Column(String, index=True)
    dis_price_by_unit = Column(Float)

    recipes = relationship("Recipe", back_populates="dish")
    menus = relationship("Menu", secondary = menu_dish_association, back_populates="dish_list")


    