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

#
# @router.get("/{analysis_id}", response_model=PersonalInformationSchema)
# async def get_item(analysis_id: int): # , db: get_db = Depends()):
#     return {"item_id": analysis_id}
#
#
# @router.get("/")
# async def get_all():
#     print('test')
#     return {"message": "Hello World"}
