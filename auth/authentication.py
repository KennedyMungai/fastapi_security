"""The Authentication file"""
from typing import Optional

from tortoise.exceptions import DoesNotExist

from auth.password import verify_password
from models.models import (AccessToken, AccessTokenTortoise, UserDb,
                           UserTortoise)


async def authenticate(email: str, password: str) -> Optional[UserDb]:
    """The function that authenticates the user

    Args:
        email (str): The user's email
        password (str): The user's password

    Returns:
        Optional[UserDb]: The user's data
    """
    try:
        user = await UserTortoise.get(email=email)
    except DoesNotExist:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return UserDb.from_orm(user)


async def create_access_token(user: UserDb) -> AccessToken:
    """The function that creates the access tokens

    Args:
        user (UserDb): The user logging in

    Returns:
        AccessToken: The schema for the access token
    """
    access_token = AccessToken(user_id=user.id)
    access_token_tortoise = await AccessTokenTortoise.create(**access_token.dict())
    
    return AccessToken.from_orm(access_token_tortoise)