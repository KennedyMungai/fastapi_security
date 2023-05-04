"""The password script"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """The hashing function 

    Args:
        password (str): The password provided by the user. 

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)