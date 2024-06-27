from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

SQLALCHEMY_DATABASE_URL = 'postgresql://%(db_user)s:%(db_passwd)s@%(db_host)s:%(db_port)s/%(db_name)s' % {
    "db_user": environ.get("DB_USER", 'myuser'),
    "db_passwd": environ.get("DB_PASSWD", 'myuserpassword'),
    "db_host": environ.get("DB_HOST", 'localhost'),
    "db_port": environ.get("DB_PORT", '5432'),
    "db_name": environ.get("DB_NAME", 'mydbname'),
}

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()