from sqlalchemy import Enum, Column, Integer, ForeignKey, date
from infrastructure.db.database import Base
import enum


class Dish(Base):
    __tablename__ = "dish"

    men_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dis_id_fk = Column(Integer, ForeignKey("dishes.dis_id"), index=True)
    men_date = Column(date)

    