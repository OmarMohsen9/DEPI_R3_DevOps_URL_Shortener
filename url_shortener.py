from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import string, random, os, time

# ---- Prometheus imports ----
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# ---- Local imports ----
from database import Base, engine, get_db
from models import URL

# ---- DB setup ----
Base.metadata.create_all(bind=engine)

# ---- App setup ----
BASE_URL = os.getenv("BASE_URL", "http://localhost:9000")
api = FastAPI()

# ---- Define Prometheus Metrics ----
url_shortened_count = Counter(
    "url_shortened_total", "Number of URLs successfully shortened"
)
redirect_success_count = Counter(
    "redirect_success_total", "Number of successful redirects"
)
lookup_failed_count = Counter(
    "lookup_failed_total", "Number of failed lookups (404 errors)"
)
request_latency = Histogram(
    "request_latency_seconds", "Request latency in seconds", ["endpoint"]
)

# ---- Models ----
class UrlBase(BaseModel):
    long_url: HttpUrl = Field(..., max_length=512, description="Provided valid HTTP/HTTPS URL")


class UrlShorten(UrlBase):
    pass


class UrlResponse(UrlBase):
    short_url: HttpUrl = Field(..., max_length=512, description="Shortened URL")


class UrlDBEntry(BaseModel):
    id: int
    short_code: str
    long_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Utility ----
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


# ---- Middleware for request latency ----
@api.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        return response
    finally:
        latency = time.time() - start
        request_latency.labels(endpoint=request.url.path).observe(latency)


# ---- Routes ----
@api.post("/shorten", response_model=UrlResponse)
def shorten_url(request: UrlShorten, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_entry = URL(short_code=short_code, long_url=str(request.long_url))
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    # Increment metric
    url_shortened_count.inc()

    return UrlResponse(
        long_url=new_entry.long_url,
        short_url=f"{BASE_URL}/{new_entry.short_code}",
    )

# ---- Prometheus Metrics Endpoint ----
@api.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@api.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not entry:
        lookup_failed_count.inc()
        raise HTTPException(status_code=404, detail="Short URL not found")

    entry.clicks += 1
    db.commit()

    redirect_success_count.inc()

    return RedirectResponse(url=entry.long_url, status_code=307)


@api.get("/admin/urls", response_model=List[UrlDBEntry])
def get_all_urls(db: Session = Depends(get_db)):
    return db.query(URL).all()




# ---- Serve static frontend ----
api.mount("/", StaticFiles(directory="static", html=True), name="static")
