"""The security endpoint file"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import APIKeyHeader

API_TOKEN = "some_secret_api_key"

security_endpoint = APIRouter(prefix="/security_endpoint", tags=["Security"])

api_key_header = APIKeyHeader(name="Token")


@security_endpoint.get("/")
async def secured_endpoint(token: str = Depends(api_key_header)):
    """A simple test endpoint for security authentication

    Args:
        token (str, optional): The security token. Defaults to Depends(api_key_header).

    Raises:
        HTTPException: The Data type for an HTTP error

    Returns:
        _type_: _description_
    """
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")

    return {"Looks like": " you are authorized"}
