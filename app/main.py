from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1 import cars 
from app.api.v1.auth.register import router as auth_router
from app.api.v1.auth.login import router as login_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(login_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(cars.router, prefix="/api/v1", tags=["Cars"])

@app.get("/")
def read_root():
    return {"status": "System work"}
