from fastapi import APIRouter

from .schemas.personal_information_schema import PersonalInformationSchema
from .risk_analysys_service import RiskAnalysisService
from .schemas.risk_score import RiskProfile

router = APIRouter(
    prefix="/risk-analysis",
    tags=["Risk Analysis"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=RiskProfile)
async def run_risk_analysis(subject: PersonalInformationSchema):
    return RiskAnalysisService().run_risk_analysis(subject)

