from fastapi import APIRouter, FastAPI

app = FastAPI()

v1 = APIRouter(
    prefix="/v1",
)
# v1.include_router(token)
# v1.include_router(users)
app.include_router(v1)
