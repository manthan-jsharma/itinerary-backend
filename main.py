from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import engine, get_db
from .seed import seed_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Thailand Travel Itinerary API",
    description="API for managing travel itineraries in Thailand",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    seed_data()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Thailand Travel Itinerary API"}



@app.get("/itineraries/", response_model=schemas.ItineraryListResponse)
def read_itineraries(
    skip: int = 0, 
    limit: int = 100, 
    num_nights: Optional[int] = None,
    regions: Optional[str] = None,
    db: Session = Depends(get_db)
):
    itineraries = crud.get_itineraries(db, skip=skip, limit=limit, num_nights=num_nights, regions=regions)
    total = crud.count_itineraries(db, num_nights=num_nights, regions=regions)
    return {"itineraries": itineraries, "total": total}



@app.get("/itineraries/{itinerary_id}", response_model=schemas.ItineraryResponse)
def read_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    itinerary = crud.get_itinerary(db, itinerary_id=itinerary_id)
    if itinerary is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return {"itinerary": itinerary}


@app.post("/recommendations/", response_model=schemas.ItineraryListResponse)
def get_recommendations(request: schemas.RecommendationRequest, db: Session = Depends(get_db)):
    itineraries = crud.get_recommended_itineraries(
        db, 
        num_nights=request.num_nights, 
        regions=request.regions,
        budget=request.budget
    )
    return {"itineraries": itineraries, "total": len(itineraries)}
