from datetime import date
from enum import Enum
from typing import NewType, Literal, Union

from pydantic import BaseModel, Field, EmailStr, SecretStr

from core.schemas.token import Token


class User(BaseModel):
    username: str = Field(
        title="User unique identifier", max_length=100, min_length=5
    )
    email: EmailStr
    date_of_birth: date | None
    first_name: str = Field(
        default=None, min_length=3, max_length=150
    )
    last_name: str = Field(
        default=None, min_length=3, max_length=150
    )
    active: bool = Field(
        default=True, title="Status of user activity",
        description="False == DEAD & Inactive user > He will be deleted soon"
    )


class UserInDB(User):
    password: SecretStr = Field(
        title="Password which will be to authorize/identify user", max_length=500, min_length=8
    )


class Data(BaseModel):

    user: User
    token: Token


class Status(str, Enum):

    successful = "Successful"
    unsuccessful = "Unsuccessful"


class UserReg(BaseModel):
    status: Status
    data: Data


username = NewType("username", str)
