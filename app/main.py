"""The entrypoint to the application"""
from fastapi import FastAPI
from app.security_endpoint import security_endpoint

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
