from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status, Header, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.config import cfgparser
from src.core import Postgres, User, UserInDB, Token, username, TokenUser, APIRouter, get_user_from_db_by_login
from src.core import delete_user_from_db_by_login, insert_user_to_db, UserReg, Status, Data, Validators

user = APIRouter(
    prefix="/user"
)
parser = cfgparser('v1.ini', 'Secrets')
db = Postgres()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/token", description="Bearer token to perform privileged actions",
)

auth_header = Header(
    alias="Authorization",
    description="Replace {token} with your token to execute this query",
    example="Bearer {token}"
)


async def verify_auth_header(header: str = auth_header):
    if header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing"
        )


def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_that_user_in_db(login: Union[EmailStr, username]) -> UserInDB | None:
    user = get_user_from_db_by_login(db, login)
    return UserInDB(**dict(user)) if user else None


def authenticate_user(login: str, plain_password: str) -> UserInDB | bool:
    user = check_that_user_in_db(login)
    if not user:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, parser.get('secret_key'))
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, parser.get('secret_key'))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_user = TokenUser(username=username)
    except JWTError:
        raise credentials_exception
    user = check_that_user_in_db(login=token_user.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user.post(
    "/token",
    response_model=Token,
    tags=['user'],
    response_description="Token to do privileged actions. Put it to your header in format:"
                         " 'Authorization: Bearer {token}'"
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user using username and password

    - **username**: unique user identifier (Could be both email or login)
    - **password**: just password

    return **token**
    """
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


@me.get("/", response_model=User, dependencies=[Depends(verify_auth_header)], tags=['user'])
async def get_user_data(current_user: User = Depends(get_current_active_user)):
    return current_user


@me.delete(
    '/delete',
    dependencies=[Depends(verify_auth_header)],
    tags=['user'],
    response_description='Successful removing',
)
async def delete_user(current_user: UserInDB = Depends(get_current_user)):
    if not delete_user_from_db_by_login(db, current_user.username):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User wasn't found in db > It can't be removed or already removed"
        )
    return {"Status": "Successful removing"}


@user.post(
    '/new',
    response_model=UserReg,
    status_code=status.HTTP_201_CREATED,
    tags=['user'],
    response_description='Successful user creation'
)
@Validators.user_exists
async def create_new_user(user: UserInDB):
    user_credentials = user.copy()
    user.password = get_password_hash(user.password)
    if not insert_user_to_db(db, user):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problems with DB. Contact technical support"
        )
    token: Token = await login_for_access_token(user_credentials)
    return {'status': Status.successful, 'data': Data(token=token, user=user)}
