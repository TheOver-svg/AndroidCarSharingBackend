from fastapi import APIRouter, Depends, HTTPException, Response
import app.models.car as models
from app.schemas.car import CarResponse, LatLngSchema, CarCreate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.car import GasolineCar, ElectricCar 
from app.api.deps import get_current_user
from app.models.trip import Trip
from app.api import deps
from app.models.trip import Trip
from app.models.car import Car  
from app.models.user import User
from app.services.pdf_service import generate_rental_contract_pdf

router = APIRouter()

@router.get("/cars", response_model=list[CarResponse])
def get_all_cars(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    active_trips = db.query(Trip.car_id).filter(Trip.status == "active").all()
    active_car_ids = [trip[0] for trip in active_trips]

    if active_car_ids:
        db_cars = db.query(models.Car).filter(models.Car.id.notin_(active_car_ids)).all()
    else:
        db_cars = db.query(models.Car).all()

    result = []
    for car in db_cars:
        car_dict = {
            "id": str(car.id),
            "model": car.model,
            "transmission": car.transmission,
            "price": car.price,
            "engine_type": car.engine_type,
            "plate_number": car.plate_number,
            "location": LatLngSchema(latitude=car.latitude, longitude=car.longitude),
            "description": car.description,
            "fuel_level": getattr(car, "fuel_level", None),
            "battery_level": getattr(car, "battery_level", None),
        }
        result.append(car_dict)
        
    return result

@router.post("/create_car", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    existing_car = db.query(models.Car).filter(models.Car.plate_number == car.plate_number).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Машина з таким номером вже існує!")
        
    if car.engine_type == "electric":
        new_car = ElectricCar(battery_level=car.battery_level)
    elif car.engine_type == "gasoline":
        new_car = GasolineCar(fuel_level=car.fuel_level)
    else:
        raise HTTPException(status_code=400, detail="Невідомий тип двигуна")

    new_car.model = car.model
    new_car.transmission = car.transmission
    new_car.price = car.price
    new_car.plate_number = car.plate_number
    new_car.description = car.description
    new_car.latitude = car.location.latitude
    new_car.longitude = car.location.longitude

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    
    return {
        "id": str(new_car.id),
        "model": new_car.model,
        "transmission": new_car.transmission,
        "price": new_car.price,
        "engine_type": new_car.engine_type,
        "plate_number": new_car.plate_number,
        "description": new_car.description,
        "fuel_level": getattr(new_car, "fuel_level", None),
        "battery_level": getattr(new_car, "battery_level", None), 
        "location": {"latitude": new_car.latitude, "longitude": new_car.longitude}
    }
    
@router.post("/cars/{car_id}/book")
def book_car(car_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машину не знайдено")

    active_trip = db.query(Trip).filter(Trip.car_id == car_id, Trip.status == "active").first()
    if active_trip:
        raise HTTPException(status_code=400, detail="Машина вже заброньована")
    
    new_trip = Trip(
        user_id=current_user["user_id"],
        car_id=car_id,
        status="active"
    )
    
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return {
        "id": new_trip.id,           
        "car_id": new_trip.car_id,
        "status": new_trip.status,
        "car_model": car.model       
    }
    
@router.get("/trips/{trip_id}/contract.pdf")
def get_trip_contract_pdf(
    trip_id: int,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    if trip.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
        
    car = db.query(Car).filter(Car.id == trip.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
        
    user_db = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    pdf_bytes = generate_rental_contract_pdf(user=user_db, car=car, trip=trip)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=contract_{trip_id}.pdf"
        }
    )