from pydantic import BaseModel, EmailStr
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    id: int

class Book(BookCreate):
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    id: int

class Customer(CustomerCreate):
    class Config:
        orm_mode = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None