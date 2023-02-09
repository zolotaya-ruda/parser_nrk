from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine('mysql+pymysql://root:83Linedip@localhost/parser_nkr')
engine.connect()

base = declarative_base()
session = Session(bind=engine)
