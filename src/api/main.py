# src/api/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from src.core.formwork_engine import run_formwork_engine

app = FastAPI(
    title="Formwork BoQ AI Engine",
    description="ML-driven formwork demand & kitting system",
    version="10.3"
)

# 🔹 Input schema
class ProjectInput(BaseModel):
    owner: str
    project_type: str
    area: float
    floors: int
    duration_days: int


# 🔹 Health check
@app.get("/")
def health_check():
    return {"status": "API is running", "phase": "10.3"}


# 🔹 Core prediction endpoint
@app.post("/predict-formwork")
def predict_formwork(data: ProjectInput):
    return run_formwork_engine(data.dict())