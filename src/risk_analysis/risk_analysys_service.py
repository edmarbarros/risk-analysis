from .schemas.personal_information_schema import PersonalInformationSchema
from .risk_calculator import RiskCalculator
from .schemas.risk_score import RiskProfile


class RiskAnalysisService:

    def __init__(self) -> None:
        pass

    def run_risk_analysis(self, subject: PersonalInformationSchema) -> RiskProfile:
        return RiskCalculator(subject).calculate_subject_score()
