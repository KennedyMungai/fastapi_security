"""The entrypoint to the application"""
from fastapi import FastAPI, status, HTTPException
from app.security_endpoint import security_endpoint
from models.models import UserCreate, User, UserDb, UserTortoise
from auth.password import get_password_hash

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    return User.from_orm(user_tortoise)