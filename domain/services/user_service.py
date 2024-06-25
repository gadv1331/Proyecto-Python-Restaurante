from infrastructure.db.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from domain.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self,user):
        hashed_password = pwd_context.hash(user.password)
        user = UserCreate(
            username= user.username,
            email= user.email,
            password= hashed_password,
            role= user.role
        )
        return self.user_repository.create_user(user)