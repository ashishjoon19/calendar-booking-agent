from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    timestamp: datetime
    is_user: bool

class BookingRequest(BaseModel):
    title: str
    start_datetime: str
    duration_minutes: int = 60
    description: Optional[str] = ""

class BookingResponse(BaseModel):
    success: bool
    message: str
    event_id: Optional[str] = None

class AvailabilityRequest(BaseModel):
    start_date: str
    end_date: str

class AvailabilityResponse(BaseModel):
    available_slots: List[str]
    busy_slots: List[str]