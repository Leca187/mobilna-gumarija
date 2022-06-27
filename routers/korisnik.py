from fastapi import APIRouter, Depends, Response, HTTPException, Path, status
import database, models
from sqlalchemy.orm import Session
import schemas
from hashing import Hash

router = APIRouter()

@router.post("/korisnik/", response_model = schemas.PokaziKorisnika, tags=["users"])
def kreiraj_nalog(korisnik: schemas.Korisnik, db: Session = Depends(database.get_db)):
    
    novi_korisnik = schemas.Korisnik(ime=korisnik.ime, email=korisnik.email, password=Hash.bcrypt(korisnik.password))
    db.add(novi_korisnik)
    db.commit()
    db.refresh(novi_korisnik)
    return novi_korisnik

@router.get("/korisnik/{korisnik_id}", response_model = schemas.PokaziKorisnika, response_model_exclude_unset=True, tags=["users"])
def pokazi_korisnika(korisnik_id: int, response: Response, db: Session = Depends(database.get_db)):
    
    korisnik = db.query(models.Korisnik).filter(models.Korisnik.id == korisnik_id).first()
    
    if not korisnik:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"message": f"Korisnik {korisnik_id} nije nadjen"}
    return korisnik