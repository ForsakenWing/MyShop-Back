from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import cfgparser


CONFIG = cfgparser()
username, password, db_name, hostname = CONFIG['user'], CONFIG['password'], CONFIG['dbname'], CONFIG['hostname']
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{hostname}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
