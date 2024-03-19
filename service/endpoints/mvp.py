from fastapi import APIRouter, HTTPException
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
    try:
        today = datetime.date.today()
        if sop_request.cliffPeriod is not None:
            possible_buying_start_point = (
                sop_request.agreementStartDate
                + relativedelta(months=sop_request.cliffPeriod)
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

        vested_percentage = min(months_passed / sop_request.vestingPeriod, 1)

        vested_shares = sop_request.numberOfAllocatedShares * vested_percentage
        return SopResponse(
            company_name=sop_request.companyName,
            vested_shares=round(vested_shares, 2),
            start_date=sop_request.agreementStartDate,
            current_data=str(today),
            note="possible to buy.",
            number_of_allocated_shares=sop_request.numberOfAllocatedShares,
        )
    except Exception as e:
        import traceback

        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
