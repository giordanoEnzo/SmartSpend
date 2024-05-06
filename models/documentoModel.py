from utils.db import db, Base

class Ssdc(Base):
    __tablename__ = 'ssdc'
    id = db.Column(db.Integer, primary_key=True)
    SSTITU = db.Column(db.String())
    SSORIG = db.Column(db.String())
    SSPROC = db.Column(db.String())
    SSQTTK = db.Column(db.Integer())

    def __init__(self, SSTITU, SSORIG, SSPROC, SSQTTK):
        self.SSTITU = SSTITU
        self.SSORIG = SSORIG
        self.SSPROC = SSPROC
        self.SSQTTK = SSQTTK

    @classmethod
    def ler_documentos(cls):
        return cls.query.all()
