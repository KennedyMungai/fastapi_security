"""The security endpoint file"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import APIKeyHeader

APP_TOKEN = "some_secret_api_key"

security_endpoint = APIRouter("/security", tags=["Security"])

api_key_header = APIKeyHeader(name="Token")


@security_endpoint.get("/")
async def security_endpoint(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid API Key")
    
    return {"Looks like": " you are authorized"}