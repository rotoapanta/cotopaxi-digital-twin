from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class SensorPoint(BaseModel):
    time: datetime
    values: Dict[str, float]

class LastPoint(BaseModel):
    measurement: str
    values: Dict[str, float]
