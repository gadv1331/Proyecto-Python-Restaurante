from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
    role: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
