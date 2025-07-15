from pydantic import BaseModel

class BookingCreated(BaseModel):
    booking_id: int
    user_id: int
    restaurant_id: int
    slot_id: int
