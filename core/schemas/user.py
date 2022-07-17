from datetime import date

from pydantic import BaseModel, Field, EmailStr, SecretStr


class UserAuth(BaseModel):
    username: str = Field(
        title="User unique identifier", max_length=100, min_length=5
    )
    password: SecretStr = Field(
        title="Password which will be to authorize/identify user", max_length=500, min_length=8
    )


class UserReg(UserAuth):
    email: EmailStr
    date_of_birth: date | None
    first_name: str = Field(
        default="", min_length=3, max_length=150
    )
    last_name: str = Field(
        default="", min_length=3, max_length=150
    )
