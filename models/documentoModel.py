from sqlalchemy import Column, Integer, String
from utils.db import Base, db

class Ssdc(Base):
    __tablename__ = 'ssdc'
    id = Column(Integer, primary_key=True)
    SSTITU = Column(String)
    SSORIG = Column(String)
    SSPROC = Column(String)
    SSQTTK = Column(Integer)

    def __init__(self, SSTITU, SSORIG, SSPROC, SSQTTK):
        self.SSTITU = SSTITU
        self.SSORIG = SSORIG
        self.SSPROC = SSPROC
        self.SSQTTK = SSQTTK

    @classmethod
    def ler_documentos(cls):
        session = db()
        documentos = session.query(cls).all()
        return documentos