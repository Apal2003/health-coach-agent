from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class MedicalHistory:
    conditions: List[str]
    medications: List[str]
    allergies: List[str]
    past_procedures: List[str]

@dataclass
class WellnessData:
    date: datetime
    sleep_hours: float
    exercise_minutes: int
    water_intake_ml: int
    stress_level: int  # 1-10
    mood: str
    notes: str