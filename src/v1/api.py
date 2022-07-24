from fastapi import FastAPI
from src.core import APIRouter

from .endpoints import user, me

app = FastAPI()

api = APIRouter(
    prefix="/api"
)

v1 = APIRouter(
    prefix="/v1",
)
user.include_router(me)
v1.include_router(user)
api.include_router(v1)
app.include_router(api)
