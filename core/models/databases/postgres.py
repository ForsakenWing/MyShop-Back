import functools
import logging

import psycopg2

from core.config import config


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
            parser = config()
            conn = None
            try:
                conn: psycopg2._psycopg.connection = psycopg2.connect(**parser)
            except Exception:
                conn.rollback()
                logging.error("Database connection error")
                raise
            else:
                cursor: psycopg2._psycopg.cursor = conn.cursor()
                result = func(query, cursor, *args, **kwargs)
                conn.commit()
            finally:
                conn.close()
            return result

        return wrapper


class Postgres(DataBase):

    @staticmethod
    @PostgresExtension.connector
    def execute(query, *args, cursor: psycopg2._psycopg.cursor = None, **kwargs):
        if args or kwargs:
            ...
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError:
            logging.error("Error while executing this query")
        else:
            logging.info("Query was successfully executed")
            return cursor.fetchall()
