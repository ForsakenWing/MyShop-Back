from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from src.core.schemas.token import Token


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
    is_active: bool = Field(
        default=True, title="Status of user activity",
        description="False == DEAD & Inactive user > He will be deleted soon"
    )


class UserInDB(User):
    password: str = Field(
        title="password field", max_length=500,
        min_length=8, description="min_length=8, max_length=500 (Only hash will be saved)"
    )

    class Config:
        orm_mode = True


class Data(BaseModel):

    user: User
    token: Token


class Status(str, Enum):

    successful = "Successful"
    unsuccessful = "Unsuccessful"


class UserReg(BaseModel):
    status: Status
    data: Data
