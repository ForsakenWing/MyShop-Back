from fastapi import APIRouter

user = APIRouter(
    prefix="/user"
)


@user.post('/create')
async def create_user():
    return {"Status": "Fail"}
