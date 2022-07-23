from core import UserInDB, Postgres
from fastapi import HTTPException, status
from core import get_user_from_db_by_login
from functools import wraps


db = Postgres()


class Validators:

    @staticmethod
    def user_exists(func):
        @wraps(func)
        async def wrapper(user: UserInDB):
            if get_user_from_db_by_login(db, user.username) or get_user_from_db_by_login(db, user.email):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User with this email or username already exists"
                )
            return await func(user)
        return wrapper
