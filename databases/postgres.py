from databases.config import config
from databases.db import DataBase
import psycopg2
import logging
import functools


class Postgres(DataBase):

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


class BaseUser:

    @staticmethod
    @Postgres.connector
    def write(query, cursor: psycopg2._psycopg.cursor = None, *args, **kwargs):
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError:
            logging.error("Error while executing this query")
        else:
            logging.info("Query was successfully executed")

    @staticmethod
    @Postgres.connector
    def read(query, cursor: psycopg2._psycopg.cursor = None, *args, **kwargs):
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError:
            logging.error("Error while executing this query")
        else:
            logging.info("Query was successfully executed")
            return cursor.fetchone()
