from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import cfgparser


CONFIG = cfgparser()
username, password, db_name = CONFIG['user'], CONFIG['password'], CONFIG['dbname']
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@localhost/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
