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


class UserCliente(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True
        from_orm = True
        orm_mode = True
