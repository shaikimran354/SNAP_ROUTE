from pydantic import BaseModel
from typing import Optional

class RouteRequest(BaseModel):
    source: str
    destination: str

class RouteResult(BaseModel):
    source: str
    destination: str
    distance_meters: float
    duration_minutes: float
    steps: int
    calories: int

class ClassifyResult(BaseModel):
    predicted_location: str