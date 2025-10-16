from fastapi import FastAPI,HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, HttpUrl
import string, random,os
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from fastapi.staticfiles import StaticFiles

from database import Base, engine, get_db
from models import URL

Base.metadata.create_all(bind=engine)  # create db if doesnt exist

BASE_URL = os.getenv("BASE_URL", "http://localhost:9000") # local testing change in deployment

api = FastAPI()


class UrlBase(BaseModel):
    long_url:HttpUrl = Field(..., max_length=512, description='Provided Valid HTTP/HTTPS URL')


# post input
class UrlShorten(UrlBase):
    pass


# post response
class UrlResponse(UrlBase):
    short_url:HttpUrl = Field(..., max_length=512, description='Full shortened URL pointing to the service endpoint')


class UrlDBEntry(BaseModel):
    id: int
    short_code: str
    long_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@api.post("/shorten", response_model=UrlResponse)
def shorten_url(request: UrlShorten, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_entry = URL(short_code=short_code, long_url=str(request.long_url))
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return UrlResponse(
        long_url=new_entry.long_url,
        short_url=f"{BASE_URL}/{new_entry.short_code}"
    )


@api.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    entry.clicks += 1  # increment counts for /metrics later
    db.commit()

    return RedirectResponse(url=entry.long_url, status_code=307)


@api.get("/admin/urls", response_model=List[UrlDBEntry])
def get_all_urls(db: Session = Depends(get_db)):
    return db.query(URL).all()


api.mount("/",StaticFiles(directory="static", html=True), name="static")
