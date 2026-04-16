from pydantic import BaseModel, Field
from typing import Optional

class LatLngSchema(BaseModel):
    latitude: float
    longitude: float

class CarCreate(BaseModel):
    model: str
    transmission: str
    price: int
    plate_number: str
    description: str
    location: LatLngSchema
    engine_type: str 
    fuel_level: Optional[int] = None 
    battery_level: Optional[int] = None

class CarResponse(BaseModel):
    id: str
    model: str
    transmission: str
    price: int
    plateNumber: str = Field(validation_alias="plate_number")
    description: str
    engineType: str = Field(validation_alias="engine_type")
    
    fuelLevel: Optional[int] = Field(default=None, validation_alias="fuel_level")
    batteryLevel: Optional[int] = Field(default=None, validation_alias="battery_level")
    
    location: LatLngSchema

    class Config:
        from_attributes = True