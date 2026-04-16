from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(50), index=True)
    transmission = Column(String(20))
    price = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    plate_number = Column(String(20), unique=True)
    description = Column(String(255))
    
    engine_type = Column(String(20))
    
    __mapper_args__ = {
        
        "polymorphic_on": engine_type,
        "polymorphic_identity": "base_car"
    }
class GasolineCar(Car):
    fuel_level = Column(Integer) 

    __mapper_args__ = {
        "polymorphic_identity": "gasoline" 
    }

class ElectricCar(Car):
    battery_level = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "electric"
    }