"""The entrypoint to the application"""
from typing import cast

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import timezone
from tortoise.exceptions import DoesNotExist

from app.security_endpoint import security_endpoint
from auth.authentication import (AccessToken, AccessTokenTortoise,
                                 authenticate, create_access_token)
from auth.password import get_password_hash
from models.models import User, UserCreate, UserTortoise, UserDb

app = FastAPI()


@app.get(
    "/",
    tags=["root"],
    name="Root",
    description="Root of the API"
)
async def root() -> dict[str, str]:
    """The root of the API

    Returns:
        dict[str, str]: A dict with the words hello world
    """
    return {"Hello": "World"}

app.include_router(security_endpoint)


@app.post(
    "/register", 
    status_code = status.HTTP_201_CREATED, 
    name="The user registration endpoint", 
    description="This is the endpoint used to register users", 
    tags=['Users']
    )
async def register(user: UserCreate) -> User:
    """Register a new user

    Args:
        user (UserCreate): The user to register

    Returns:
        User: The registered user
    """
    hashed_password = get_password_hash(user.password)
   
    try:
        user_tortoise = await UserTortoise.create(**user.dict(), hashed_password=hashed_password)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists"
            )
    
    return User.from_orm(user_tortoise)


@app.post("/token", name="The token endpoint", description="The endpoint that provides the token for the application", status_code=status.HTTP_200_OK, tags=['Users'])
async def create_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    """The token creation endpoint

    Args:
        form_data (OAuth2PasswordRequestForm, optional): The form data to log in to the endpoint. Defaults to Depends(OAuth2PasswordRequestForm).

    Raises:
        HTTPException: The exception class for fastapi exceptions

    Returns:
        dict: A dictionary of the access token and the token type (In this case it is the bearer token)
    """
    email = form_data.username
    password = form_data.password
    user = await authenticate(email, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
    token = await create_access_token(user)
    
    return {"access_token": token.access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl = "/token"))
    ) -> UserTortoise:
    """This is a function that gets the current user logged in to the application

    Args:
        token (str, optional): The access token for the user. Defaults to Depends(OAuth2PasswordBearer(tokenUrl = "/token")).

    Raises:
        HTTPException: The exception handling class for the fastapi endpoints

    Returns:
        UserTortoise: The template for the User data using the tortoise ORM
    """
    try:
        access_token: AccessTokenTortoise = await AccessTokenTortoise.get(access_token=token, expiration_date__gte=timezone.now()).prefetch_related('user')

        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
            )
        
        

@app.get(
    "/protected-route", 
    name="The protected route", 
    description="The protected route for the application", 
    tags=['Users'], 
    response_model=User
    )
async def protected_route(
    user: UserDb = Depends(get_current_user)
    ):
    """The protected route for the application

    Args:
        user (UserDb, optional): The user to get the data from. Defaults to Depends(get_current_user).

    Returns:
        User: The user data
    """
    return User.from_orm(user)