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
from infrastructure.security.oauth2 import get_current_admin_user
from domain.schemas.user import UserCreate, User
from typing import List
#gestion de inventario
from domain.schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from domain.services.ingredient_service import IngredientService
from infrastructure.db.repositories.ingredient_repository import IngredientRepository

router = APIRouter()

@router.post("/auth_user")
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user


@router.post("/user_register", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return user_service.create_user(user)

@router.get("/chef")
def get_chef_message(current_user:UserSchema = Depends(get_current_chef_user)):
    return {"message": "Hola, soy un chef"}

@router.get("/camarero")
def get_camarero_message(current_user: UserSchema = Depends(get_current_camarero_user)):
    return {"message": "Hola, soy un camarero"}

@router.get("/cliente")
def get_cliente_message(current_user: UserSchema = Depends(get_current_cliente_user)):
    return {"message": "Hola, soy un cliente"}

@router.get("/admin")
def get_admin_message(current_user: UserSchema = Depends(get_current_admin_user)):
    return {"message": "Hola, soy un admin"}

#-----------------------------------------------
#ENDPOINTS PARA GESTION DE INVENTARIO
#----------------------------------------------

@router.post("/ingredients/", response_model = Ingredient)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    return ingredient_service.create_ingredient(ingredient)

@router.put("/ingredients/", response_model = Ingredient)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    updated_ingredient = ingredient_service.update_ingredient(ingredient_id, ingredient)
    if updated_ingredient:
        return updated_ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")

@router.delete("/ingredients/", response_model = Ingredient)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    deleted_ingredient = ingredient_service.delete_ingredient(ingredient_id)
    if deleted_ingredient:
        return deleted_ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")

@router.get("/ingredients/", response_model = List[Ingredient])
def get_all_ingredients(db: Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    return ingredient_service.get_all_ingredients()

@router.get("/ingredients/{ingridient_id}", response_model = Ingredient)
def get_ingredient(ingredient_id: int, db:Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    ingredient = ingredient_service.get_ingridient_by_id(ingredient_id)
    if ingredient:
        return ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")