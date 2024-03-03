from pydantic import BaseModel
from datetime import date
from typing import Optional


class SopAgreement(BaseModel):
    company_name: str
    agreement_start_date: date
    cliff_period: Optional[int]  # months
    number_of_allocated_shares: int
    vesting_period: int  # months
    vesting_percentage: float


class SopResponse(BaseModel):
    company_name: str
    start_date: date
    current_data: date
    vested_shares: float
    note: Optional[str]
