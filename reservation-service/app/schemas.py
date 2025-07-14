from pydantic import BaseModel
from datetime import datetime


class SlotOut(BaseModel):
    id: int
    restaurant_id: int
    start_time: datetime
    end_time: datetime
    is_available: bool

    model_config = {"from_attributes": True}


class BookingCreate(BaseModel):
    user_id: int
    restaurant_id: int
    slot_id: int


class BookingOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    slot_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
