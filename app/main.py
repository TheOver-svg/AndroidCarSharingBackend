from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1 import cars 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(cars.router, prefix="/api/v1", tags=["Cars"])

@app.get("/")
def read_root():
    return {"status": "Система працює!"}