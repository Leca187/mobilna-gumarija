# daj mi sve razlicite brendove
# u postmanu testirati search sve moguce varijante i sve ostalo
from fastapi import FastAPI, Depends
import models
from database import engine
from typing import Optional
from routers import magacin, korisnik

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(magacin.router)
app.include_router(korisnik.router)

# garaza = {

#     1:{
#         "vrstaGume": "putnicka",
#         "brend": "sava",
#         "sezona": "zimska",
#         "sirina": "195",
#         "visina": "65",
#         "precnik": "16",
#         "indexBrzine": "Q",
#     },

#     2:{
#         "vrstaGume": "putnicka",
#         "brend": "sava",
#         "sezona": "zimska",
#         "sirina": "205",
#         "visina": "55",
#         "precnik": "15",
#         "indexBrzine": "Q",
#     }

# }

# @app.get("/magacin/pretrazi")
# def pretrazi_gume(vrstaGume: Optional[str] = None, brend: Optional[str] = None, sezona: Optional[str] = None,
#                 sirina: Optional[str] = None, visina: Optional[str] = None, precnik: Optional[str] = None, indexBrzine: Optional[str] = None):
#     gume = []
#     for guma_id in garaza:
#         if garaza[guma_id]["vrstaGume"] == vrstaGume or vrstaGume == None:
#             if garaza[guma_id]["brend"] == brend or brend == None:
#                 if garaza[guma_id]["sezona"] == sezona or sezona == None:
#                     if garaza[guma_id]["sirina"] == sirina or sirina == None:
#                         if garaza[guma_id]["visina"] == visina or visina == None:
#                             if garaza[guma_id]["precnik"] == precnik or precnik == None:
#                                 if garaza[guma_id]["indexBrzine"] == indexBrzine or indexBrzine == None:
#                                     gume.append(garaza[guma_id])
#     return gume

