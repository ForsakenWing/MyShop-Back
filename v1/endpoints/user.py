from datetime import datetime, timedelta
from typing import Union

import aiohttp
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config import cfgparser
from core import Postgres, User, UserInDB, Token, username, TokenData, APIRouter
from core import delete_user_from_db_by_login, insert_user_to_db, UserReg, Status, Data
from core import post_async

user = APIRouter(
    prefix="/user"
)

parser = cfgparser('v1.ini', 'Secrets')
db = Postgres()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", description="Bearer token to perform privileged actions"
)


def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_that_user_in_db(login: Union[EmailStr, username]):
    from core import get_user_from_db_by_login
    user_in_db = get_user_from_db_by_login(db, login)
    return UserInDB(**user_in_db) if user_in_db else None


def authenticate_user(login: str, password: str) -> UserInDB | None:
    user = check_that_user_in_db(login)
    if not user:
        return False
    if not verify_password(password, user.password.get_secret_value()):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, parser.get('secret_key'))
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, parser.get('secret_key'))
        subject: str = payload.get("sub")
        if subject is None:
            raise credentials_exception
        token_data = TokenData(login=subject)
    except JWTError:
        raise credentials_exception
    user_in_db = check_that_user_in_db(login=token_data.login)
    if user_in_db is None:
        raise credentials_exception
    return user_in_db


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(parser.get('access_token_expire_minutes')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

me = APIRouter(
    prefix="/me",
    redirect_slashes=True
)


@me.get("/", response_model=User)
async def get_user_data(current_user: User = Depends(get_current_active_user)):
    return current_user


@me.delete('/delete')
async def delete_user(current_user: User = Depends(get_current_user)):
    if not delete_user_from_db_by_login(db, current_user.username):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User wasn't found in db > It cant be removed or already removed"
        )
    return {"Status": "User was successfully removed from the system", "User": User}


@user.post('/new', response_model=UserReg)
async def create_new_user(user: UserInDB):
    plain_password = user.password.get_secret_value()
    user.password = get_password_hash(plain_password)
    if check_that_user_in_db(user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this email already exists"
        )
    if check_that_user_in_db(user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this username already exists"
        )
    if not insert_user_to_db(db, user):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problems with DB. Contact technical support"
        )
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8088/api/v1/user/token"
        token = await post_async(
            url, session, body={
                'username': user.username,
                'password': plain_password
            }
        )
    return {'status': Status.successful, 'data': Data(token=token, user=user)}
