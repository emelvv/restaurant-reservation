import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Base, engine, SessionLocal
from .schemas import SlotOut, BookingCreate, BookingOut
from .crud import get_available_slots, create_booking
from .rabbit import publish_booking_created

app = FastAPI(title="Reservation Service")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/reservations/available", response_model=list[SlotOut])
def available(restaurant_id: int, db: Session = Depends(get_db)):
    return get_available_slots(db, restaurant_id)


@app.post("/reservations/book", response_model=BookingOut)
def book(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        db_booking = create_booking(db, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    publish_booking_created({
        "booking_id": db_booking.id,
        "user_id": db_booking.user_id,
        "restaurant_id": db_booking.restaurant_id,
        "slot_id": db_booking.slot_id
    })
    return db_booking
