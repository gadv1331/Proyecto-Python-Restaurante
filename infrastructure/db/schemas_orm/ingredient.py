from sqlalchemy import Enum, Column, Integer, String, Float
from infrastructure.db.database import Base
import enum

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    quantity = Column(Float)