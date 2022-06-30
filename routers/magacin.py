from fastapi import APIRouter, Depends, Response, status
from pip import List
import database, models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()


@router.get("/magacin/", status_code=status.HTTP_200_OK, tags=["magacin"])
def pokazi_gume(vrstaGume: Optional[str] = None, brend: Optional[str] = None, sezona: Optional[str] = None, sirina: Optional[str] = None, visina: Optional[str] = None,
                    precnik: Optional[str] = None, indexBrzine: Optional[str] = None, db: Session = Depends(database.get_db)):
    
    SveGume = db.query(models.magacin).all()
    razGume = []
    
    for guma_id in SveGume:
        if guma_id.vrstaGume == vrstaGume or vrstaGume == None:
            if guma_id.brend == brend or brend == None:
                if guma_id.sezona == sezona or sezona == None:
                    if guma_id.sirina == sirina or sirina == None:
                        if guma_id.visina == visina or visina == None:
                            if guma_id.precnik == precnik or precnik == None:
                                if guma_id.indexBrzine == indexBrzine or indexBrzine == None:
                                    razGume.append(guma_id)
    return razGume
               
    return razGume
    
@router.get("/magacin/brend", status_code=status.HTTP_200_OK, tags=["magacin"])
def pokazi_sve_brendove(db: Session = Depends(database.get_db)):
    
    razGume = []
    SveGume = db.query(models.magacin).all()
    print(SveGume)

    for brend_gume in SveGume:
        if brend_gume.brend not in razGume:
            razGume.append(brend_gume.brend)
            print(brend_gume.brend)
    return razGume

@router.get("/magacin/{guma_id}", tags=["magacin"])
def pokazi_gumu(guma_id: int, response: Response, db: Session = Depends(database.get_db), get_current_user: schemas.Korisnik = Depends(oauth2.get_current_user)):
    
    Guma = db.query(models.magacin).filter(models.magacin.id == guma_id).first()
    
    if not Guma:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"Guma {guma_id} nije nadjena"}
    return Guma    

@router.post("/magacin/", status_code=status.HTTP_201_CREATED, tags=["magacin"])
def kreiraj_gumu(guma: schemas.Guma, db: Session = Depends(database.get_db), get_current_user: schemas.Korisnik = Depends(oauth2.get_current_user)):   
    
    nova_guma = models.magacin(vrstaGume=guma.vrstaGume, brend=guma.brend, sezona=guma.sezona, sirina=guma.sirina, visina=guma.visina, precnik=guma.precnik, 
                               indexBrzine=guma.indexBrzine, kolicina=guma.kolicina)
    db.add(nova_guma)
    db.commit()
    db.refresh(nova_guma)
    return nova_guma

@router.put("/magacin/{guma_id}", status_code=status.HTTP_202_ACCEPTED, tags=["magacin"])
def izmeni_gumu(guma_id: int, response: Response, guma: schemas.UpdateGuma, db: Session = Depends(database.get_db), get_current_user: schemas.Korisnik = Depends(oauth2.get_current_user)):
    
    IzGuma = db.query(models.magacin).filter(models.magacin.id == guma_id)
    
    if not IzGuma.first():
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"Guma {guma_id} nije nadjena"}

    if guma.vrstaGume != None:
        IzGuma.first().vrstaGume = guma.vrstaGume
        
    if guma.brend != None:
        IzGuma.first().brend = guma.brend
    
    if guma.sezona != None:
        IzGuma.first().sezona = guma.sezona
    
    if guma.sirina != None:
        IzGuma.first().sirina = guma.sirina
    
    if guma.visina != None:
        IzGuma.first().visina = guma.visina
   
    if guma.precnik != None:
        IzGuma.first().precnik = guma.precnik
    
    if guma.indexBrzine != None:
        IzGuma.first().indexBrzine = guma.indexBrzine
   
    if guma.kolicina != None:
        IzGuma.first().kolicina = guma.kolicina
    
    guma = {

        "vrstaGume": IzGuma.first().vrstaGume,
        "brend": IzGuma.first().brend,
        "sezona": IzGuma.first().sezona,
        "sirina": IzGuma.first().sirina,
        "visina": IzGuma.first().visina,
        "precnik": IzGuma.first().precnik,
        "indexBrzine": IzGuma.first().indexBrzine,
        "kolicina": IzGuma.first().kolicina
    }

    IzGuma.update(guma)
    db.commit()
    
    return {"message": f"Guma {guma_id} je izmenjena"}

@router.delete("/magacin/{guma_id}", tags=["magacin"])
def izbrisi_gumu(guma_id: int, response: Response, db: Session = Depends(database.get_db), get_current_user: schemas.Korisnik = Depends(oauth2.get_current_user)):
    
    if db.query(models.magacin).filter(models.magacin.id == guma_id).first() not in db.query(models.magacin).all():
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"Guma {guma_id} ne postoji"}
    
    db.query(models.magacin).filter(models.magacin.id == guma_id).delete(synchronize_session=False)
    
    db.commit()   

    return {"Message": "Guma izbrisana"}

# __istrazi distinct__
# u postmanu testirati search sve moguce varijante i sve ostalo