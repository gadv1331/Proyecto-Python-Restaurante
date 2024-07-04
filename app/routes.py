from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from domain.services.auth_service import AuthService
from domain.services.user_service import UserService
from domain.services.dish_service import DishService
from domain.services.menu_service import MenuService
from domain.services.order_service import OrderService
from domain.services.ingredient_service import IngredientService
from infrastructure.db.database import get_db
from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.db.repositories.dish_repository import DishRepository
from infrastructure.db.repositories.menu_repository import MenuRepository
from infrastructure.db.repositories.order_repository import OrderRepository
from infrastructure.db.repositories.ingredient_repository import IngredientRepository
from domain.schemas.user import User as UserSchema
from infrastructure.security.oauth2 import get_current_chef_user
from infrastructure.security.oauth2 import get_current_camarero_user
from infrastructure.security.oauth2 import get_current_cliente_user
from infrastructure.security.oauth2 import get_current_admin_user
from domain.schemas.user import UserCreate, User, UserCliente
from domain.schemas.dish import Dish, DishCreate
from domain.schemas.menu import Menu, MenuCreate
from domain.schemas.recipe import Recipe, RecipeCreate
from domain.schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from domain.schemas.order import Order, OrderCreate, OrderUpdate
from infrastructure.exceptions.exce_user import UserAlreadyExistsException

router = APIRouter()

# --------------------------------
# ENDPOINTS PARA VERIFICACION DEL USUARIO
# --------------------------------

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

# --------------------------------
# ENDPOINTS DE USUARIOS
# --------------------------------

@router.post("/user_register", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    try:
        created_user = user_service.create_user(user)
        return created_user
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

@router.get("/get_users_clientes/", response_model= List[UserCliente])
def get_clients(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    clientes = user_service.get_users_by_role("cliente")
    if not clientes:
        raise HTTPException(
            status_code=404,
            detail="No clients found"
        )
    return clientes
# --------------------------------
# ENDPOINTS PARA VERIFICAR LOS ROLES DE USUARIO
# --------------------------------

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
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    return ingredient_service.create_ingredient(ingredient)

@router.put("/ingredients/", response_model = Ingredient)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    updated_ingredient = ingredient_service.update_ingredient(ingredient_id, ingredient)
    if updated_ingredient:
        return updated_ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")

@router.put("/ingredients/update_quantity", response_model = Ingredient)
def update_quantity(ingredient_id: int, quantity_change: float, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    update_ingredient = ingredient_service.update_quantity(ingredient_id, quantity_change)
    if update_ingredient:
        return update_ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")

@router.delete("/ingredients/", response_model = Ingredient)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    deleted_ingredient = ingredient_service.delete_ingredient(ingredient_id)
    if deleted_ingredient:
        return deleted_ingredient
    raise HTTPException(status_code = 404, detail = "Ingrediente no encontrado")

@router.get("/ingredients/", response_model = List[Ingredient])
def get_all_ingredients(db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    ingredient_repository = IngredientRepository(db)
    ingredient_service = IngredientService(ingredient_repository)
    return ingredient_service.get_all_ingredients()

@router.get("/ingredients/{ingridient_id}", response_model = Ingredient)
def get_ingredient(ingredient_id: int, db:Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
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
def create_dish(dish: DishCreate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    return dish_service.create_dish(dish)

@router.put("/dishes/{dish_id}", response_model = Dish)
def update_dish(dish_id: int, dish: DishCreate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    updated_dish = dish_service.update_dish(dish_id, dish)
    if updated_dish:
        return updated_dish
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.delete("/dishes/{dish_id}", response_model=Dish)
def delete_dish(dish_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    deleted_dish = dish_service.delete_dish(dish_id)
    if deleted_dish:
        return Dish.from_orm(deleted_dish)
    raise HTTPException(status_code=404, detail="Plato no encontrado")

@router.get("/dishes/{dish_id}", response_model = Dish)
def get_dish(dish_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    dish = dish_service.get_dish(dish_id)
    if dish:
        return Dish.from_orm(dish)
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.get("/dishes/", response_model = List[Dish])
def get_all_dishes(db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    dishes = dish_service.get_all_dishes()
    return [Dish.from_orm(dish) for dish in dishes]

#RECETAS

@router.post("/dishes/{dish_id}/recipes/", response_model = Recipe)
def add_recipe_to_dish(dish_id: int, ingredient_id: int, quantity: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    added_recipe = dish_service.add_recipe_to_dish(dish_id, ingredient_id, quantity)
    if added_recipe:
        return added_recipe
    raise HTTPException(status_code = 404, detail = "Plato no encontrado")

@router.put("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def update_recipe_of_dish(dish_id: int, recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    updated_recipe = dish_service.update_recipe_of_dish(dish_id, recipe_id, recipe)
    if updated_recipe:
        return updated_recipe
    raise HTTPException(status_code = 404, detail = "Plato o receta no encontrados")

@router.delete("/dishes/{dish_id}/recipes/{recipe_id}", response_model = Recipe)
def remove_recipe_from_dish(dish_id: int, recipe_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_reository = DishRepository(db)
    dish_service = DishService(dish_reository)
    removed_recipe = dish_service.remove_recipe_from_dish(dish_id, recipe_id)
    if removed_recipe:
        return Recipe.from_orm(removed_recipe)
    raise HTTPException(status_code=404, detail="Receta o plato no encontrados")

@router.get("/dishes/{dish_id}/recipes/", response_model = List[Recipe])
def get_recipes_of_dish(dish_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    dish_repository = DishRepository(db)
    dish_service = DishService(dish_repository)
    recipes = dish_service.get_recipes_of_dish(dish_id)
    return [Recipe.from_orm(recipe) for recipe in recipes]

# MENUS

@router.post("/menus/", response_model = Menu)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    return menu_service.create_menu(menu)

@router.post("/menus/{menu_id}/dishes/{dish_id}", response_model = Menu)
def add_dish_to_menu(menu_id: int, dish_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    added_dish = menu_service.add_dish_to_menu(menu_id, dish_id)
    if added_dish:
        return Menu.from_orm(added_dish)
    raise HTTPException(status_code = 404, detail = "Menu o plato no encontrados")

@router.delete("/menus/{menu_id}/dishes/{dish_id}", response_model = Menu)
def remove_dish_from_menu(menu_id: int, dish_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    removed_dish = menu_service.remove_dish_from_menu(menu_id, dish_id)
    if removed_dish:
        return Menu.from_orm(removed_dish)
    raise HTTPException(status_code=404, detail="Menu o plato no encontrados")

@router.get("/menus/{menu_id}", response_model = Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    menu = menu_service.get_menu(menu_id)
    if menu:
        return Menu.from_orm(menu)
    raise HTTPException(status_code = 404, detail = "Menu no encontrado")

@router.get("/menus/", response_model = List[Menu])
def get_all_menus(db: Session = Depends(get_db), current_user:UserSchema = Depends(get_current_chef_user)):
    menu_repository = MenuRepository(db)
    menu_service = MenuService(menu_repository)
    menus = menu_service.get_all_menus()
    return [Menu.from_orm(menu) for menu in menus]

# --------------------------------
# ENDPOINTS PARA ORDENES
# --------------------------------

@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    return order_service.create_order(order)

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@router.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    updated_order = order_service.update_order(order_id, order_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return updated_order

@router.get("/orders/user/{user_id}", response_model=List[Order])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    orders = order_service.get_orders_by_user(user_id)
    return orders

@router.get("/orders/dish/{dish_id}", response_model=List[Order])
def get_orders_by_dish(dish_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    orders = order_service.get_orders_by_dish(dish_id)
    return orders

@router.get("/orders/", response_model=List[Order])
def get_all_orders(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    orders = order_service.get_all_orders()
    return orders

@router.delete("/orders/{order_id}", response_model=Order)
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    deleted_order = order_service.delete_order(order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return deleted_order

@router.post("/orders/{order_id}/dishes/{dish_id}", response_model=Order)
def add_dish_to_order(order_id: int, dish_id: int,db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_camarero_user)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    updated_order = order_service.add_dish_to_order(order_id, dish_id)
    if updated_order:
        return updated_order
    else:
        raise HTTPException(status_code=404, detail="Orden o plato no encontrado.")


