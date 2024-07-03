from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.user import User as UserModel
from domain.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError
from infrastructure.exceptions.exc_user import UserAlreadyExistsException

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    #def create_user(self, user: UserCreate):
    #    db_user = UserModel(**user.dict())
    #    self.db.add(db_user)
    #    self.db.commit()
    #    self.db.refresh(db_user)
    #    return db_user
    
    def create_user(self, user: UserCreate):
        db_user = UserModel(**user.dict())
        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsException("User already exists")