from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.security.jwt_handler import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
 
    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if not user or not verify_password(password, user.password):
            return None
        return user

    def create_access_token_for_user(self, user):
        return create_access_token(data={"sub": user.username, "role": user.role})
    