from pydantic import BaseModel, Field
from typing import List
from datetime import date


class TripCreate(BaseModel):
    name: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    members: List[str] = Field(..., min_length=1)


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    paid_by: str = Field(..., min_length=1)
    shared_by: List[str] = Field(..., min_length=1)
    date: date
    description: str | None = None