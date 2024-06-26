from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from domain.services.auth_service import AuthService
from domain.services.user_service import UserService
from infrastructure.db.database import get_db
from infrastructure.db.repositories.user_repository import UserRepository
from domain.schemas.user import User as UserSchema
from infrastructure.security.oauth2 import get_current_active_user
from infrastructure.security.oauth2 import get_current_chef_user
from infrastructure.security.oauth2 import get_current_camarero_user
from infrastructure.security.oauth2 import get_current_cliente_user
from domain.schemas.user import UserCreate, User

router = APIRouter()

@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token_for_user(user)
    print("token creado:",access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user


@router.post("/registro_usuario", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.create_user(user)

@router.get("/chef")
def get_chef_message(current_user: UserSchema = Depends(get_current_chef_user)):
    return {"message": "Hola, soy un chef"}

@router.get("/camarero")
def get_camarero_message(current_user: UserSchema = Depends(get_current_chef_user)):
    return {"message": "Hola, soy un camarero"}

@router.get("/cliente")
def get_cliente_message(current_user: UserSchema = Depends(get_current_chef_user)):
    return {"message": "Hola, soy un cliente"}

