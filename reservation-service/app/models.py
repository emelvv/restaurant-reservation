import os
from sqlalchemy import (
    create_engine, Column, Integer,
    ForeignKey, DateTime, Boolean, String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=True)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    slot = relationship("Slot")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
