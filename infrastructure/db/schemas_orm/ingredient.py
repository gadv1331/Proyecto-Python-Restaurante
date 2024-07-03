from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    quantity = Column(Float)

    recipes = relationship("Recipe", back_populates = "ingredient")