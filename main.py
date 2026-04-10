from fastapi import FastAPI

app = FastAPI()

@app.get("/cars")
def getCars():
    return {1,2,3,4}
