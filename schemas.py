from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

# Base schemas
class LocationBase(BaseModel):
    name: str
    region: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AccommodationBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    price_per_night: float
    rating: Optional[float] = None
    amenities: Optional[str] = None
    image_url: Optional[str] = None

class TransferBase(BaseModel):
    type: str
    duration_minutes: int
    price: float
    description: Optional[str] = None

class ActivityBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    duration_minutes: int
    price: float
    rating: Optional[float] = None
    image_url: Optional[str] = None

class ItineraryBase(BaseModel):
    name: str
    description: Optional[str] = None
    num_nights: int
    regions: str

# Create schemas
class ItineraryCreate(ItineraryBase):
    pass

# Read schemas
class Location(LocationBase):
    id: int
    
    class Config:
        orm_mode = True

class Accommodation(AccommodationBase):
    id: int
    location_id: int
    location: Location
    
    class Config:
        orm_mode = True

class Transfer(TransferBase):
    id: int
    from_location_id: int
    to_location_id: int
    from_location: Location
    to_location: Location
    
    class Config:
        orm_mode = True

class Activity(ActivityBase):
    id: int
    location_id: int
    location: Location
    
    class Config:
        orm_mode = True

class ItineraryDay(BaseModel):
    day_number: int
    accommodation: Optional[Accommodation] = None
    activities: List[Activity] = []
    transfers: List[Transfer] = []
    
    class Config:
        orm_mode = True

class Itinerary(ItineraryBase):
    id: int
    total_price: float
    is_recommended: bool
    days: List[ItineraryDay] = []
    
    class Config:
        orm_mode = True

# Response schemas
class ItineraryResponse(BaseModel):
    itinerary: Itinerary
    
    class Config:
        orm_mode = True

class ItineraryListResponse(BaseModel):
    itineraries: List[Itinerary]
    total: int
    
    class Config:
        orm_mode = True

# Request schemas
class ItineraryDayRequest(BaseModel):
    day_number: int
    accommodation_id: Optional[int] = None
    activity_ids: List[int] = []
    transfer_ids: List[int] = []

class ItineraryRequest(BaseModel):
    name: str
    description: Optional[str] = None
    num_nights: int = Field(..., ge=1, le=14)
    regions: str
    days: List[ItineraryDayRequest] = []

# Recommendation request
class RecommendationRequest(BaseModel):
    num_nights: int = Field(..., ge=1, le=14)
    regions: Optional[str] = None
    budget: Optional[float] = None
