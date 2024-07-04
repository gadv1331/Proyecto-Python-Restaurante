from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.user import User as UserModel
from domain.schemas.user import UserCreate
from infrastructure.exceptions.exce_user import UserAlreadyExistsException
from sqlalchemy.exc import IntegrityError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def create_user(self, user: UserCreate) -> UserModel:
        db_user = UserModel(**user.dict())
        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsException("User already exists")
    
    def get_users_by_role(self, role: str) -> list[UserModel]:
        return self.db.query(UserModel).filter(UserModel.role == role).all()