"""The models file"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """The base model for the user"""
    email: EmailStr
    
    class Config:
        """The configuration subclass for the User base model
        """
        orm_mode = True



class UserCreate(UserBase):
    """The UserCreate Schema

    Args:
        UserBase (BaseModel): The base class for the users
    """
    password: str
    
    
class User(UserBase):
    """The User schema

    Args:
        UserBase (BaseModel): The schema for the users
    """
    id: int