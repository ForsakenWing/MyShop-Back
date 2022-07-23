import functools
import logging
from typing import Union

import psycopg2
from psycopg2.extras import DictCursor
from pydantic import PositiveInt, EmailStr

from config import cfgparser
from core.schemas.user import username, UserInDB


class DataBase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


class PostgresExtension:

    @staticmethod
    def connector(func):
        @functools.wraps(func)
        def wrapper(query, *args, **kwargs):
            parser = cfgparser()
            conn = None
            try:
                conn: psycopg2._psycopg.connection = psycopg2.connect(**parser)
            except Exception:
                conn.rollback()
                logging.error("Database connection error")
                raise
            else:
                cursor: psycopg2._psycopg.cursor = conn.cursor(cursor_factory=DictCursor)
                result = func(query, *args, cursor=cursor, **kwargs)
                conn.commit()
            finally:
                conn.close()
            return result

        return wrapper


class Postgres(DataBase):

    @staticmethod
    @PostgresExtension.connector
    def _execute(
            query,
            *args,
            cursor: psycopg2._psycopg.cursor = None,
            fetch_one: bool = False,
            fetch_all: bool = False,
            fetch_many: PositiveInt = False,
            **kwargs
    ):
        if args or kwargs:
            ...
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as err:
            print(err)
            logging.error("Error while executing this query")
        else:
            logging.info("Query was successfully executed")
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            elif fetch_many:
                return cursor.fetchmany(fetch_many)

    @classmethod
    def create_tables(cls):
        cls._execute(
            '''
            CREATE TABLE IF NOT EXISTS accounts (
            user_id serial PRIMARY KEY,
            username VARCHAR ( 100 ) UNIQUE NOT NULL,
            password VARCHAR ( 500 ) NOT NULL,
            email VARCHAR ( 255 ) UNIQUE NOT NULL,
            first_name VARCHAR (150),
            last_name VARCHAR (150),
            date_of_birth DATE,
            active BOOLEAN DEFAULT TRUE, 
            created_on TIMESTAMPTZ NOT NULL DEFAULT CURRENT_DATE,
            last_login TIMESTAMPTZ,
            updated_at TIMESTAMPTZ DEFAULT CURRENT_DATE);
            '''.strip()
        )

    def select_user_from_table_accounts(self, login: Union[username, EmailStr]):
        result = self._execute(
            f"""
            SELECT username, password, email, first_name, last_name, date_of_birth FROM accounts 
            WHERE username = '{login}' OR email = '{login}';
            """,
            fetch_one=True
        )
        return result

    def delete_user_from_table_accounts(self, login: Union[username, EmailStr]):
        result = self._execute(
            f"""
            DELETE FROM accounts WHERE username = '{login}' or email = '{login}'
            RETURNING *;
            """,
            fetch_one=True
        )
        return result

    def insert_user_to_table_accounts(self, user: UserInDB):
        user_dict = user.dict().items()
        result = self._execute(
            f"""
            INSERT INTO accounts
            ({", ".join(map(lambda x: f'"{x}"', [key for key, value in user_dict if value]))})
            VALUES
            ({", ".join(map(lambda x: f"'{x}'", [value for key, value in user_dict if value]))})
            RETURNING user_id;
            """,
            fetch_one=True
        )
        return result


def get_user_from_db_by_login(db: Postgres, login: Union[username, EmailStr]) -> psycopg2._psycopg.cursor.fetchone:
    result = db.select_user_from_table_accounts(login)
    return result


def delete_user_from_db_by_login(db: Postgres, login: Union[username, EmailStr]) -> psycopg2._psycopg.cursor.fetchone:
    result = db.delete_user_from_table_accounts(login)
    return dict(result) if result else None


def insert_user_to_db(db: Postgres, user: UserInDB):
    result = db.insert_user_to_table_accounts(user)
    return result
