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