from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class magacin(Base):
    __tablename__ = 'gume'
    id = Column(Integer,primary_key=True, index=True)
    vrstaGume = Column(String)
    brend = Column(String)
    sezona = Column(String)
    sirina = Column(String)
    visina = Column(String)
    precnik = Column(String)
    indexBrzine = Column(String)
    kolicina = Column(Integer)

class Korisnik(Base):
    __tablename__ = 'korisnik'
    id = Column(Integer,primary_key=True, index=True)
    ime = Column(String)
    email = Column(String)
    password = Column(String)