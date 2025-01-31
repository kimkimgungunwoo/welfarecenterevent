from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DB_URL='mysql+pymysql://user:112233@localhost:3306/gjb_database'
engine = create_engine(DB_URL)

SesseionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False)

