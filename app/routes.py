from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from domain.services.auth_service import AuthService
from domain.services.user_service import UserService
from domain.services.dish_service import DishService
from infrastructure.db.database import get_db
from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.db.repositories.dish_repository import DishRepository
from domain.schemas.user import User as UserSchema
from infrastructure.security.oauth2 import get_current_active_user
from infrastructure.security.oauth2 import get_current_chef_user
from infrastructure.security.oauth2 import get_current_camarero_user
from infrastructure.security.oauth2 import get_current_cliente_user
from infrastructure.security.oauth2 import get_current_admin_user
from domain.schemas.user import UserCreate, User
from domain.schemas.dish import DishCreate, Dish
from domain.schemas.recipe import RecipeCreate, Recipe

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

# --------------------------------
# ENDPOINTS PARA MENUS, RECETAS Y PLATOS
# --------------------------------

# PLATOS

@router.post("/dishes/", response_model = Dish)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    return dish_service.create_dish(dish)

@router.put("/dishes/{dish_id}", response_model = Dish)
def update_dish(dish_id: int, dish: DishCreate, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    updated_dish = dish_service.update_dish(dish_id, dish)
    if updated_dish:
        return updated_dish
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.delete("/dishes/{dish_id}", response_model = Dish)
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    deleted_dish = dish_service.delete_dish(dish_id)
    if deleted_dish:
        return deleted_dish
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.get("/dishes/{dish_id}", response_model = Dish)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    dish = dish_service.get_dish(dish_id)
    if dish:
        return dish
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.get("/dishes/", response_model = Dish)
def get_all_dishes(db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    return dish_service.get_all_dishes()

#RECETAS

@router.post("/dishes/{dish_id}/recipes/", response_model = Recipe)
def add_recipe_to_dish(dish_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    dish_reository = dishRepository(db)
    dish_service = DishService(dish_reository)
    added_recipe = dish_service.add_recipe_to_dish(dish_id, recipe)
    if added_recipe:
        return added_recipe
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.put("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def update_recipe_in_dish(dish_id: int, recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    updated_recipe = dish_service.update_recipe_in_dish(dish_id, recipe_id, recipe)
    if updated_recipe:
        return updated_recipe
    raise HTTPException(status_code = 404, detail = "Plato o receta no encontrados")

@router.delete("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def delete_recipe_from_dish(dish_id: int, recipe_id: int, db: Session = Depends(get_db)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    deleted_recipe = dish_service.delete_recipe_from_dish(dish_id, recipe_id)
    if deleted_recipe:
        return deleted_recipe
    raise HTTPException(status_code = 404, detail = "Plato o receta no encontrados")

@router.get("/dishes/{dish_id}/recipes/", response_model = Recipe)
def get_recipe_of_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    recipes = dish_service.get_recipes_of_dish(dish_id)
    if recipes:
        return recipes
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

