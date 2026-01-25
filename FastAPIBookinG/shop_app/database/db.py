
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'postgresql://postgres:adminadmin@localhost/fast_api_booking'
engine = create_engine(DB_URL)

Sessionlocal = sessionmaker(bind=engine)

Base = declarative_base()