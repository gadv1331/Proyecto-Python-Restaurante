from sqlalchemy import Enum, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base
import enum


class Recipe(Base):
    __tablename__ = "recipes"

    rec_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dis_id_fk = Column(Integer, ForeignKey("dishes.dis_id"), index=True)
    ing_id_fk = Column(Integer, ForeignKey("ingredients.ing_id"), index=True)
    rec_quantity = Column(Integer)

    dish = relationship("Dish", back_populates="recipes")
    ingredient = relationship("Ingredient", back_populates="recipes")