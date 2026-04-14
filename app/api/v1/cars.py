from fastapi import FastAPI, APIRouter, Depends
import app.models.car as models
from app.shemas.car import CarResponse, LatLngSchema, CarCreate
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


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
            "fuel_level": car.fuel_level,
            "plate_number": car.plate_number,
            "location": LatLngSchema(latitude=car.latitude, longitude=car.longitude)
        }
        result.append(car_dict)
        
    return result


@router.post("/create_car")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    new_car = models.Car(
        model=car.model,
        transmission=car.transmission,
        price=car.price,
        fuel_level=car.fuel_level,
        plate_number=car.plate_number,
        latitude=car.location.latitude,
        longitude=car.location.longitude
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return {
        "id": str(new_car.id),
        "model": new_car.model,
        "transmission": new_car.transmission,
        "price": new_car.price,
        "fuel_level": new_car.fuel_level,
        "plate_number": new_car.plate_number,
        "location": LatLngSchema(latitude=new_car.latitude, longitude=new_car.longitude)
    }

app.include_router(router)