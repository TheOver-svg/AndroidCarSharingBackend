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
    fuel_level = Column(Integer)
    plate_number = Column(String(20), unique=True)