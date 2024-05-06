from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URI = "postgresql://postgres:HareWare%402024@0.tcp.sa.ngrok.io:13018/SmartSpend"

engine = create_engine(DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))
