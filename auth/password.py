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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """The verification function

    Args:
        plain_password (str): The password provided by the user.
        hashed_password (str): The hashed password.

    Returns:
        bool: The verification result.
    """
    return pwd_context.verify(plain_password, hashed_password)