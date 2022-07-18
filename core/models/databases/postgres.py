import functools
import logging

import psycopg2

from config import cfgparser


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

    # Re-check
    # @classmethod
    # def create_tables(cls):
    #     cls.execute(
    #         '''
    #         CREATE TABLE [IF NOT EXISTS] accounts (
    #         user_id serial PRIMARY KEY,
    #         username VARCHAR ( 50 ) UNIQUE NOT NULL,
    #         password VARCHAR ( 50 ) NOT NULL,
    #         email VARCHAR ( 255 ) UNIQUE NOT NULL,
    #         created_on TIMESTAMP NOT NULL,
    #         last_login TIMESTAMP );
    #         '''
    #     )
