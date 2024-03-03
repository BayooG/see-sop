from fastapi import APIRouter, Response
from service.models import SopAgreement, SopResponse
import datetime
from dateutil.relativedelta import relativedelta


router = APIRouter(prefix="/mvp")


@router.post(
    "/calculate",
    tags=["mvp"],
    summary="calculate single SOP agreement state",
    response_model=SopResponse,
)
def calculate(sop_request: SopAgreement):
    today = datetime.date.today()
    if sop_request.cliff_period is not None:
        possible_buying_start_point = sop_request.agreement_start_date + relativedelta(
            month=sop_request.cliff_period
        )

        if today < possible_buying_start_point:
            return SopResponse(
                company_name=sop_request.company_name,
                vested_shares=0,
                start_date=sop_request.agreement_start_date,
                current_data=today,
                note="buying is not possible yet!",
            )

    delta = relativedelta(today, sop_request.agreement_start_date)
    months_passed = delta.years * 12 + delta.months
    vesting_amount = sop_request.number_of_allocated_shares * (
        (months_passed // sop_request.vesting_period) * sop_request.vesting_percentage
    )

    return SopResponse(
        company_name=sop_request.company_name,
        vested_shares=vesting_amount,
        start_date=sop_request.agreement_start_date,
        current_data=today,
        note="possible to buy.",
    )
