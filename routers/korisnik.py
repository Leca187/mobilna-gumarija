from fastapi import APIRouter, Depends, Response, HTTPException, Path, status
import database, models, ltoken
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas
from hashing import Hash
import token

router = APIRouter()

@router.post("/korisnik/", response_model = schemas.PokaziKorisnika, tags=["users"])
def kreiraj_nalog(korisnik: schemas.Korisnik, db: Session = Depends(database.get_db)):
    
    novi_korisnik = models.Korisnik(ime=korisnik.ime, email=korisnik.email, password=Hash.bcrypt(korisnik.password))
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

@router.post("/korisik/login")
def login(response: Response, Login:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.Korisnik).filter(models.Korisnik.email == Login.username).first()
    if not user:
        
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"message": "Invalid username"}
    
    if not Hash.verify(user.password, Login.password):

        response.status_code=status.HTTP_404_NOT_FOUND
        return{"message": "Invalid password"}


    access_token = ltoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}