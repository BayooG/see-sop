from pydantic import BaseModel
from datetime import date
from typing import Optional


class SopAgreement(BaseModel):
    companyName: str
    agreementStartDate: date
    cliffPeriod: Optional[int]  # months
    numberOfAllocatedShares: int
    vestingPeriod: int  # months
    vestingPercentage: Optional[float]  # months


class SopResponse(BaseModel):
    company_name: str
    start_date: date
    current_data: date
    vested_shares: float
    note: Optional[str]
    number_of_allocated_shares: int
