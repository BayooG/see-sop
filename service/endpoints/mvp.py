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
    if sop_request.cliffPeriod is not None:
        possible_buying_start_point = sop_request.agreementStartDate + relativedelta(
            month=sop_request.cliffPeriod
        )

        if today < possible_buying_start_point:
            return SopResponse(
                company_name=sop_request.companyName,
                vested_shares=0,
                start_date=sop_request.agreementStartDate,
                current_data=today,
                note="buying is not possible yet!",
            )

    delta = relativedelta(today, sop_request.agreementStartDate)
    months_passed = delta.years * 12 + delta.months
    vesting_amount = sop_request.numberOfAllocatedShares * (
        (months_passed // sop_request.vestingPeriod) * sop_request.vestingPercentage
    )
    if vesting_amount > sop_request.numberOfAllocatedShares:
        vesting_amount = sop_request.numberOfAllocatedShares

    return SopResponse(
        company_name=sop_request.companyName,
        vested_shares=vesting_amount,
        start_date=sop_request.agreementStartDate,
        current_data=today,
        note="possible to buy.",
        number_of_allocated_shares=sop_request.numberOfAllocatedShares,
    )
