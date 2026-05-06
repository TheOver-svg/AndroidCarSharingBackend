from fastapi import APIRouter, Depends, HTTPException
import app.models.car as models
from app.schemas.car import CarResponse, LatLngSchema, CarCreate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.car import GasolineCar, ElectricCar 
from app.api.deps import get_current_user
from app.models.trip import Trip

router = APIRouter()

@router.get("/trips/all")
def get_all_trips_admin(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # В ідеалі тут має бути перевірка на admin статус користувача
    trips = db.query(Trip).all()
    
    result = []
    for trip in trips:
        result.append({
            "trip_id": trip.id,
            "user_name": trip.user.full_name,
            "user_email": trip.user.email,
            "car_model": trip.car.model,
            "status": trip.status,
            "start_time": trip.start_time
        })
    return result

@router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машину не знайдено")
    db.delete(car)
    db.commit()
    return {"message": "Машину видалено"}