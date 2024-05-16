from sqlalchemy import Column, Integer, String, LargeBinary
from utils.db import Base, db


class Ssdc(Base):
    __tablename__ = 'ssdc'
    id = Column(Integer, primary_key=True)
    sstitu = Column(String)
    ssqttk = Column(Integer)
    sspdfo = Column(LargeBinary)
    sspdfp = Column(LargeBinary)

    def __init__(self, sstitu, ssqttk, sspdfo, sspdfp):
        self.sstitu = sstitu
        self.ssqttk = ssqttk
        self.sspdfo = sspdfo
        self.sspdfp = sspdfp

    @classmethod
    def ler_documentos(cls):
        session = db()
        documentos = session.query(cls).all()
        return documentos

    @classmethod
    def gravar_documento(cls, sstitu, ssqttk, sspdfo, sspdfp):
        session = db()
        documento = cls(sstitu=sstitu, ssqttk=ssqttk, sspdfo=sspdfo, sspdfp=sspdfp)
        session.add(documento)
        session.commit()
