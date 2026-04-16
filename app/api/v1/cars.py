from fastapi import FastAPI, APIRouter, Depends, HTTPException
import app.models.car as models
from app.shemas.car import CarResponse, LatLngSchema, CarCreate
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.car import GasolineCar, ElectricCar 

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cars", response_model=list[CarResponse])
def get_all_cars(db: Session = Depends(get_db)):
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
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    
    existing_car = db.query(models.Car).filter(models.Car.plate_number == car.plate_number).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Машина з таким номером вже існує!")
    if car.engine_type == "electric":
        new_car = ElectricCar(
            battery_level=car.battery_level
        )
    elif car.engine_type == "gasoline":
        new_car = GasolineCar(
            fuel_level=car.fuel_level
        )
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

app.include_router(router)