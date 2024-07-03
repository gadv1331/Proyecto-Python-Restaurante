from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from domain.services.auth_service import AuthService
from domain.services.user_service import UserService
from domain.services.dish_service import DishService
from domain.services.menu_service import MenuService
from infrastructure.db.database import get_db
from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.db.repositories.dish_repository import DishRepository
from infrastructure.db.repositories.menu_repository import MenuRepository
from domain.schemas.user import User as UserSchema
from infrastructure.security.oauth2 import get_current_active_user
from infrastructure.security.oauth2 import get_current_chef_user
from infrastructure.security.oauth2 import get_current_camarero_user
from infrastructure.security.oauth2 import get_current_cliente_user
from infrastructure.security.oauth2 import get_current_admin_user
from domain.schemas.user import UserCreate, User

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

@router.put("/ingredients/update_quantity", response_model = Ingredient)
def update_quantity(ingredient_id: int, quantity_change: float, db: Session = Depends(get_db)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    update_ingredient = ingredient_service.update_quantity(ingredient_id, quantity_change)
    if update_ingredient:
        return update_ingredient
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

@router.delete("/dishes/{dish_id}", response_model=Dish)
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    deleted_dish = dish_service.delete_dish(dish_id)
    if deleted_dish:
        return Dish.from_orm(deleted_dish)
    raise HTTPException(status_code=404, detail="Plato no encontrado")

@router.get("/dishes/{dish_id}", response_model = Dish)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    dish = dish_service.get_dish(dish_id)
    if dish:
        return Dish.from_orm(dish)
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.get("/dishes/", response_model = List[Dish])
def get_all_dishes(db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    dishes = dish_service.get_all_dishes()
    return [Dish.from_orm(dish) for dish in dishes]

#RECETAS

@router.post("/dishes/{dish_id}/recipes/", response_model = Recipe)
def add_recipe_to_dish(dish_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    added_recipe = dish_service.add_recipe_to_dish(dish_id, recipe)
    if added_recipe:
        return added_recipe
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.put("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def update_recipe_of_dish(dish_id: int, recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    updated_recipe = dish_service.update_recipe_of_dish(dish_id, recipe_id, recipe)
    if updated_recipe:
        return updated_recipe
    raise HTTPException(status_code = 404, detail = "Plato o receta no encontrados")

@router.delete("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def remove_recipe_from_dish(dish_id: int, recipe_id: int, db: Session = Depends(get_db)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    removed_recipe = dish_service.remove_recipe_from_dish(dish_id, recipe_id)
    if removed_recipe:
        return Recipe.from_orm(removed_recipe)
    raise HTTPException(status_code=404, detail="Receta o plato no encontrados")

@router.get("/dishes/{dish_id}/recipes/", response_model = List[Recipe])
def get_recipes_of_dish(dish_id: int, db: Session = Depends(get_db)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    recipes = dish_service.get_recipes_of_dish(dish_id)
    return [Recipe.from_orm(recipe) for recipe in recipes]

# MENUS

@router.post("/menus/", response_model = Menu)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    return menu_service.create_menu(menu)

@router.post("/menus/{menu_id}/dishes/{dish_id}", response_model = Menu)
def add_dish_to_menu(menu_id: int, dish_id: int, db: Session = Depends(get_db)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    added_dish = menu_service.add_dish_to_menu(menu_id, dish_id)
    if added_dish:
        return Menu.from_orm(added_dish)
    raise HTTPException(status_code = 404, detail = "Menu o plato no encontrados")

@router.delete("/menus/{menu_id}/dishes/{dish_id}", response_model = Menu)
def remove_dish_from_menu(menu_id: int, dish_id: int, db: Session = Depends(get_db)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    removed_dish = menu_service.remove_dish_from_menu(menu_id, dish_id)
    if removed_dish:
        return Menu.from_orm(removed_dish)
    raise HTTPException(status_code=404, detail="Menu o plato no encontrados")

@router.get("/menus/{menu_id}", response_model = Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    menu = menu_service.get_menu(menu_id)
    if menu:
        return Menu.from_orm(menu)
    raise HTTPException(status_code = 404, detail = "Menu no encontrado")

@router.get("/menus/", response_model = List[Menu])
def get_all_menus(db: Session = Depends(get_db)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    menus = menu_service.get_all_menus()
    return [Menu.from_orm(menu) for menu in menus]