"""The models file"""
from pydantic import BaseModel, EmailStr
from tortoise import fields, Model


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
    
    
class UserDb(User):
    """The Schema for the data to be stored in the database

    Args:
        User (UserBase): The schema for the data stored in the database
    """
    hashed_password: str


class UserTortoise(Model):
    """The User Tortoise model

    Args:
        Model (_type_): No idea
    """
    id = fields.IntField(pk=True, generated = True)
    email = fields.CharField(max_length=255, unique=True, index= True, null=False)
    hashed_password = fields.CharField(max_length=255, null=False)
    
    class Meta:
        """The meta subclass for the UserTortoise model
        """
        table = "users"