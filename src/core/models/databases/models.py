from sqlalchemy import Boolean, Column, Integer, String, Date, TIME
from datetime import time as current_date

from .database import Base


class User(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    date_of_birth = Column(Date)
    password = Column(String)
    created_on = Column(TIME, default=current_date())
    last_login = Column(TIME)
    updated_at = Column(TIME, default=current_date())
    is_active = Column(Boolean, default=True)

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
