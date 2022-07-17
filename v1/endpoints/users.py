from fastapi import APIRouter

users = APIRouter(
    prefix="/users"
)


@users.post('/create')
async def create_user():
    return {"Status": "Fail"}
