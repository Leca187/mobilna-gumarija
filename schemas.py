from pydantic import BaseModel
from typing import Optional

class Guma(BaseModel):

    vrstaGume: str
    brend: str
    sezona: str
    sirina: str
    visina: str
    precnik: str
    indexBrzine: str
    kolicina: int

class UpdateGuma(BaseModel):

    vrstaGume: Optional[str] = None
    brend: Optional[str] = None
    sezona: Optional[str] = None
    sirina: Optional[str] = None
    visina: Optional[str] = None
    precnik: Optional[str] = None
    indexBrzine: Optional[str] = None
    kolicina: Optional[int] = None

class BrendGuma(BaseModel):

    brend: str
    class Config():
        orm_mode = True

class Korisnik(BaseModel):

    ime: str
    email: str
    password: str

class PokaziKorisnika(BaseModel):

    ime: Optional[str] = None
    email: Optional[str] = None 
    message: Optional[str] = None 
    class Config():
        orm_mode = True   