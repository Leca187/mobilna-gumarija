from fastapi import APIRouter, Depends, Response, status
from pip import List
import database, models
from sqlalchemy.orm import Session
import schemas
from typing import Optional

router = APIRouter()


@router.get("/magacin/", status_code=status.HTTP_200_OK, tags=["magacin"])
def pokazi_sve_gume(db: Session = Depends(database.get_db)):
    
    SveGume = db.query(models.magacin).all()
    return SveGume

# POKAZI SAMO BRENDOVE !!! kako ne pokazati duplikate, __istrazi distinct__

# @router.get("/magacin/", response_model = List[schemas.BrendGuma], status_code=status.HTTP_200_OK)
# def pokazi_sve_gume(db: Session = Depends(database.get_db)):
    
#     SveGume = db.query(models.magacin).all()
#     return SveGume

@router.get("/magacin/pretraga")
def pretrazi_gume(vrstaGume: Optional[str] = None, brend: Optional[str] = None, db: Session = Depends(database.get_db)):
    
    gume = []
    tr = db.query(models.magacin).filter(models.magacin.vrstaGume == vrstaGume).all()
    # trr = db.query(models.magacin).filter(models.magacin.brend == brend).all()
    print(tr[2].brend)
    gumica = [tr[0].id, tr[0].vrstaGume, tr[0].brend, tr[0].sezona, tr[0].sirina, tr[0].visina, tr[0].precnik, tr[0].indexBrzine]
    print(gumica)
    
    for guma_id in tr:
        if tr[guma_id].vrstaGume == vrstaGume or vrstaGume == None:
            # if trr[guma_id][brend] == brend or brend == None:
             gume.append(tr)
    
    return gume
    


@router.get("/magacin/{guma_id}", tags=["magacin"])
def pokazi_gumu(guma_id: int, response: Response, db: Session = Depends(database.get_db)):
    
    Guma = db.query(models.magacin).filter(models.magacin.id == guma_id).first()
    
    if not Guma:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"Guma {guma_id} nije nadjena"}
    return Guma    

@router.post("/magacin/", status_code=status.HTTP_201_CREATED, tags=["magacin"])
def kreiraj_gumu(guma: schemas.Guma, db: Session = Depends(database.get_db)):   
    
    nova_guma = models.magacin(vrstaGume=guma.vrstaGume, brend=guma.brend, sezona=guma.sezona, sirina=guma.sirina, visina=guma.visina, precnik=guma.precnik, 
                               indexBrzine=guma.indexBrzine, kolicina=guma.kolicina)
    db.add(nova_guma)
    db.commit()
    db.refresh(nova_guma)
    return nova_guma

@router.put("/magacin/{guma_id}", status_code=status.HTTP_202_ACCEPTED, tags=["magacin"])
def izmeni_gumu(guma_id: int, response: Response, guma: schemas.UpdateGuma, db: Session = Depends(database.get_db)):
    
    IzGuma = db.query(models.magacin).filter(models.magacin.id == guma_id)
    
    if not IzGuma.first():
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"Message": f"Guma {guma_id} nije nadjena"}
    
    IzGuma.update(guma.dict())
    db.commit()
    
    return {"message": f"Guma {guma_id} je izmenjena"}
# izmeniti samo jedan parametar u tabeli

@router.delete("/magacin/{guma_id}", tags=["magacin"])
def izbrisi_gumu(guma_id: int, db: Session = Depends(database.get_db)):
    
    db.query(models.magacin).filter(models.magacin.id == guma_id).delete(synchronize_session=False)
    
    db.commit()   

    return {"Message": "Guma izbrisana"}
# ako guma ne postoji error pri brisanju