from pydantic import BaseModel, Field

class LatLngSchema(BaseModel):
    latitude: float
    longitude: float

class CarResponse(BaseModel):
    id: str
    model: str
    transmission: str
    price: int
    fuelLevel: int = Field(validation_alias="fuel_level") 
    plateNumber: str = Field(validation_alias="plate_number")
    location: LatLngSchema

    class Config:
        from_attributes = True
        
class CarCreate(BaseModel):
    model: str
    transmission: str
    price: int
    fuel_level: int
    plate_number: str
    location: LatLngSchema