from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from .database import Base

# Association table for many-to-many relationship between Itinerary and Accommodation
itinerary_accommodation = Table(
    'itinerary_accommodation',
    Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('itineraries.id'), primary_key=True),
    Column('accommodation_id', Integer, ForeignKey('accommodations.id'), primary_key=True),
    Column('day_number', Integer, nullable=False),
)

# Association table for many-to-many relationship between Itinerary and Transfer
itinerary_transfer = Table(
    'itinerary_transfer',
    Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('itineraries.id'), primary_key=True),
    Column('transfer_id', Integer, ForeignKey('transfers.id'), primary_key=True),
    Column('day_number', Integer, nullable=False),
)

# Association table for many-to-many relationship between Itinerary and Activity
itinerary_activity = Table(
    'itinerary_activity',
    Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('itineraries.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('day_number', Integer, nullable=False),
)

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)  # e.g., Phuket, Krabi
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationships
    accommodations = relationship("Accommodation", back_populates="location")
    activities = relationship("Activity", back_populates="location")
    transfers_from = relationship("Transfer", foreign_keys="Transfer.from_location_id", back_populates="from_location")
    transfers_to = relationship("Transfer", foreign_keys="Transfer.to_location_id", back_populates="to_location")

class Accommodation(Base):
    __tablename__ = 'accommodations'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., Hotel, Resort, Villa
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    description = Column(Text)
    price_per_night = Column(Float, nullable=False)
    rating = Column(Float)  # e.g., 4.5 out of 5
    amenities = Column(Text)  # Comma-separated list of amenities
    image_url = Column(String(255))
    
    # Relationships
    location = relationship("Location", back_populates="accommodations")
    itineraries = relationship("Itinerary", secondary=itinerary_accommodation, back_populates="accommodations")

class Transfer(Base):
    __tablename__ = 'transfers'
    
    id = Column(Integer, primary_key=True, index=True)
    from_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    to_location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., Car, Ferry, Speedboat
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    
    # Relationships
    from_location = relationship("Location", foreign_keys=[from_location_id], back_populates="transfers_from")
    to_location = relationship("Location", foreign_keys=[to_location_id], back_populates="transfers_to")
    itineraries = relationship("Itinerary", secondary=itinerary_transfer, back_populates="transfers")

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., Sightseeing, Adventure, Cultural
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float)
    image_url = Column(String(255))
    
    # Relationships
    location = relationship("Location", back_populates="activities")
    itineraries = relationship("Itinerary", secondary=itinerary_activity, back_populates="activities")

class Itinerary(Base):
    __tablename__ = 'itineraries'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    num_nights = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    is_recommended = Column(Boolean, default=False)
    regions = Column(String(100), nullable=False)  # e.g., "Phuket, Krabi"
    
    # Relationships
    accommodations = relationship("Accommodation", secondary=itinerary_accommodation, back_populates="itineraries")
    transfers = relationship("Transfer", secondary=itinerary_transfer, back_populates="itineraries")
    activities = relationship("Activity", secondary=itinerary_activity, back_populates="itineraries")
