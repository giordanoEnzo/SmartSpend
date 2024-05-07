from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = "postgresql://postgres:HareWare@2024@0.tcp.sa.ngrok.io:13018/SmartSpend"

engine = create_engine(DATABASE_URI)
Base = declarative_base()
db = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)
