"""The models file"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """The base model for the user"""
    email: EmailStr
    
    class Config:
        """The configuration subclass for the User base model
        """
        orm_mode = True
