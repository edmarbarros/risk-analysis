from .schemas.personal_information_schema import PersonalInformationSchema
from .risk_calculator import RiskCalculator
from .schemas.risk_score import RiskProfile


class RiskAnalysisService:

    risk_calculator: RiskCalculator

    def __init__(self) -> None:
        self.risk_calculator = RiskCalculator()
        pass

    def run_risk_analysis(self, subject: PersonalInformationSchema) -> RiskProfile:
        return self.risk_calculator.calculate_subject_score(subject)
