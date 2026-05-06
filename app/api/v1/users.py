from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.trip import Trip
from pydantic import BaseModel
from datetime import datetime
from app.models.car import Car

router = APIRouter()

class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None

@router.get("/me")
def get_my_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    return {
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone
    }

@router.put("/me")
def update_my_profile(data: UserProfileUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if data.full_name: user.full_name = data.full_name
    if data.phone: user.phone = data.phone
        
    db.commit()
    db.refresh(user)
    return {"message": "Профіль оновлено", "full_name": user.full_name}

@router.get("/me/trips")
def get_my_trips(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_id == current_user["user_id"]).all()
    
    result = []
    for trip in trips:
        result.append({
            "trip_id": trip.id,
            "car_model": trip.car.model, 
            "start_time": trip.start_time,
            "status": trip.status,
            "total_cost": trip.total_cost
        })
    return result

@router.post("/{trip_id}/finish")
async def finish_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip.status = "finished"
    trip.end_time = datetime.utcnow()
    car = db.query(Car).filter(Car.id == trip.car_id).first()
    if car:
        car.status = "available"
    
    db.commit()
    return {"message": "Trip finished successfully"}