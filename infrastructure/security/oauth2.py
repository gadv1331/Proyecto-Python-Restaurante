from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from infrastructure.security.jwt_handler import SECRET_KEY, ALGORITHM
from infrastructure.db.database import get_db
from sqlalchemy.orm import Session
from infrastructure.db.schemas_orm.user import User as UserModel
from domain.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth_user")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user



def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    #if not current_user.is_active:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_chef_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "chef":
        raise HTTPException(status_code=403, detail="User without the necessary permissions")
    return current_user

def get_current_camarero_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "camarero":
        raise HTTPException(status_code=403, detail="User without the necessary permissions")
    return current_user

def get_current_cliente_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "cliente":
        raise HTTPException(status_code=403, detail="User without the necessary permissions")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user