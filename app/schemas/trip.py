from pydantic import BaseModel
from datetime import datetime

class AdminTripResponse(BaseModel):
    trip_id: int
    user_name: str
    user_email: str
    car_model: str
    status: str
    start_time: datetime
    total_cost: Optional(float)= None

    class Config:
        from_attributes = True