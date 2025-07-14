from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timezone


def get_available_slots(db: Session, restaurant_id: int):
    return db.query(models.Slot).filter(
        models.Slot.restaurant_id == restaurant_id,
        models.Slot.is_available == True
    ).all()


def create_booking(db: Session, booking: schemas.BookingCreate):
    # помечаем слот занятым
    slot = db.query(models.Slot).get(booking.slot_id)
    if not slot or not slot.is_available:
        raise ValueError("Slot unavailable")
    slot.is_available = False

    db_booking = models.Booking(
        user_id=booking.user_id,
        restaurant_id=booking.restaurant_id,
        slot_id=booking.slot_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
