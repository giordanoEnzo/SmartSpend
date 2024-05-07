from sqlalchemy import Column, Integer, String
from utils.db import Base, db

class Ssdc(Base):
    __tablename__ = 'ssdc'
    id = Column(Integer, primary_key=True)
    sstitu = Column(String)
    ssorig = Column(String)
    ssproc = Column(String)
    ssqttk = Column(Integer)

    def __init__(self, sstitu, ssorig, ssproc, ssqttk):
        self.sstitu = sstitu
        self.ssorig = ssorig
        self.ssprog = ssproc
        self.ssqttk = ssqttk

    @classmethod
    def ler_documentos(cls):
        session = db()
        documentos = session.query(cls).all()
        return documentos