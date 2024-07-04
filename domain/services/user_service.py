from infrastructure.db.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from domain.schemas.user import UserCreate, User, UserCliente
from infrastructure.exceptions.exce_user import UserAlreadyExistsException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: UserCreate) -> User:
        existing_user = self.user_repository.get_user_by_username(user.email)
        if existing_user:
            raise UserAlreadyExistsException("User already exists")

        hashed_password = pwd_context.hash(user.password)
        user = UserCreate(
            username=user.username,
            email=user.email,
            password=hashed_password,
            role=user.role
        )
        return self.user_repository.create_user(user)

    def get_users_by_role(self, role: str) -> list[UserCliente]:
        users = self.user_repository.get_users_by_role(role)  
        return [UserCliente.from_orm(user) for user in users]
    
    