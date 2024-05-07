from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = "postgresql://postgres:HareWare%402024@localhost/SmartSpend"

engine = create_engine(DATABASE_URI)
Base = declarative_base()
db = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)
