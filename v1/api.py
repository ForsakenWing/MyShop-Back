from fastapi import APIRouter, FastAPI
from .endpoints import users, token

app = FastAPI()

api = APIRouter(
    prefix="/api"
)

v1 = APIRouter(
    prefix="/v1",
)

v1.include_router(token)
v1.include_router(users)
api.include_router(v1)
app.include_router(api)
