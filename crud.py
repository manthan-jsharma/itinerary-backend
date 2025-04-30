from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from typing import List, Optional, Dict
from . import models, schemas
from collections import defaultdict


def organize_itinerary_days(itinerary, db: Session):
    days = []

    accommodations = db.query(
        models.Accommodation,
        models.itinerary_accommodation.c.day_number
    ).join(
        models.itinerary_accommodation,
        models.Accommodation.id == models.itinerary_accommodation.c.accommodation_id
    ).filter(
        models.itinerary_accommodation.c.itinerary_id == itinerary.id
    ).all()

    activities = db.query(
        models.Activity,
        models.itinerary_activity.c.day_number
    ).join(
        models.itinerary_activity,
        models.Activity.id == models.itinerary_activity.c.activity_id
    ).filter(
        models.itinerary_activity.c.itinerary_id == itinerary.id
    ).all()
    
    # Get all transfers for this itinerary with day numbers
    transfers = db.query(
        models.Transfer,
        models.itinerary_transfer.c.day_number
    ).join(
        models.itinerary_transfer,
        models.Transfer.id == models.itinerary_transfer.c.transfer_id
    ).filter(
        models.itinerary_transfer.c.itinerary_id == itinerary.id
    ).all()
    

    day_data = defaultdict(lambda: {"accommodation": None, "activities": [], "transfers": []})
    
    for accommodation, day_number in accommodations:
        day_data[day_number]["accommodation"] = accommodation
    
    for activity, day_number in activities:
        day_data[day_number]["activities"].append(activity)
    
    for transfer, day_number in transfers:
        day_data[day_number]["transfers"].append(transfer)
    

    for day_number in range(1, itinerary.num_nights + 2):  # +2 because checkout day
        if day_number in day_data:
            days.append({
                "day_number": day_number,
                "accommodation": day_data[day_number]["accommodation"],
                "activities": day_data[day_number]["activities"],
                "transfers": day_data[day_number]["transfers"]
            })
        else:
            days.append({
                "day_number": day_number,
                "accommodation": None,
                "activities": [],
                "transfers": []
            })
    
    return days

# Get a specific itinerary by ID
def get_itinerary(db: Session, itinerary_id: int):
    itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if itinerary:
        itinerary.days = organize_itinerary_days(itinerary, db)
    return itinerary

def get_itineraries(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    num_nights: Optional[int] = None,
    regions: Optional[str] = None
):
    query = db.query(models.Itinerary)
    
    if num_nights is not None:
        query = query.filter(models.Itinerary.num_nights == num_nights)
    
    if regions is not None:
        # Filter itineraries that contain any of the specified regions
        for region in regions.split(','):
            region = region.strip()
            query = query.filter(models.Itinerary.regions.like(f"%{region}%"))
    
    itineraries = query.offset(skip).limit(limit).all()
    
    # Add days to each itinerary
    for itinerary in itineraries:
        itinerary.days = organize_itinerary_days(itinerary, db)
    
    return itineraries


def count_itineraries(
    db: Session, 
    num_nights: Optional[int] = None,
    regions: Optional[str] = None
):
    query = db.query(func.count(models.Itinerary.id))
    
    if num_nights is not None:
        query = query.filter(models.Itinerary.num_nights == num_nights)
    
    if regions is not None:
        # Filter itineraries that contain any of the specified regions
        for region in regions.split(','):
            region = region.strip()
            query = query.filter(models.Itinerary.regions.like(f"%{region}%"))
    
    return query.scalar()

# Create a new itinerary
def create_itinerary(db: Session, itinerary: schemas.ItineraryRequest):
    # Calculate total price based on accommodations, activities, and transfers
    total_price = 0.0
    

    db_itinerary = models.Itinerary(
        name=itinerary.name,
        description=itinerary.description,
        num_nights=itinerary.num_nights,
        total_price=total_price,  # Will update later
        is_recommended=False,
        regions=itinerary.regions
    )
    
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)
    

    for day in itinerary.days:
        # Add accommodation
        if day.accommodation_id:
            db.execute(
                models.itinerary_accommodation.insert().values(
                    itinerary_id=db_itinerary.id,
                    accommodation_id=day.accommodation_id,
                    day_number=day.day_number
                )
            )
            
            # Add accommodation price to total
            accommodation = db.query(models.Accommodation).filter(models.Accommodation.id == day.accommodation_id).first()
            if accommodation:
                total_price += accommodation.price_per_night
        

        for activity_id in day.activity_ids:
            db.execute(
                models.itinerary_activity.insert().values(
                    itinerary_id=db_itinerary.id,
                    activity_id=activity_id,
                    day_number=day.day_number
                )
            )
            

            activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
            if activity:
                total_price += activity.price
        
        # Add transfers
        for transfer_id in day.transfer_ids:
            db.execute(
                models.itinerary_transfer.insert().values(
                    itinerary_id=db_itinerary.id,
                    transfer_id=transfer_id,
                    day_number=day.day_number
                )
            )
            
            # Add transfer price to total
            transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
            if transfer:
                total_price += transfer.price
    
    # Update total price
    db_itinerary.total_price = total_price
    db.commit()
    db.refresh(db_itinerary)
    
    # Add days to the returned itinerary
    db_itinerary.days = organize_itinerary_days(db_itinerary, db)
    
    return db_itinerary

# Get recommended itineraries
def get_recommended_itineraries(
    db: Session, 
    num_nights: int,
    regions: Optional[str] = None,
    budget: Optional[float] = None
):
    query = db.query(models.Itinerary).filter(models.Itinerary.is_recommended == True)
    
    # Filter by number of nights
    if num_nights > 0:
        query = query.filter(models.Itinerary.num_nights == num_nights)
    

    if regions:
        for region in regions.split(','):
            region = region.strip()
            query = query.filter(models.Itinerary.regions.like(f"%{region}%"))
    

    if budget:
        query = query.filter(models.Itinerary.total_price <= budget)
    
    itineraries = query.all()
    

    for itinerary in itineraries:
        itinerary.days = organize_itinerary_days(itinerary, db)
    
    return itineraries