from passlib.context import CryptContext
from config import cfgparser
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter

parser = cfgparser('v1.ini', 'Secrets')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", description="Bearer token to perform privileged actions"
)

token = APIRouter(
    prefix="/token"
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str = None, email: str = None):
    ...


@token.get('/')
def some_test():
    return {"Status": "Fail"}
