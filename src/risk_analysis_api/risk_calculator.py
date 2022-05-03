import datetime

from src.risk_analysis_api.schemas.personal_information_schema import PersonalInformationSchema, OwnershipStatusEnum, \
    MaritalStatusEnum

from .schemas.risk_score import RiskProfile, RiskScoreEnum
from .risk_analysis_constants import MAX_AGE_LIMIT, MIN_AGE_LIMIT, MIN_INCOME, MIN_INCOME_THRESHOLD


class RiskCalculator:
    subject: PersonalInformationSchema

    def __init__(self, subject: PersonalInformationSchema) -> None:
        self.subject = subject
        pass

    def subject_has_mortgaged_house(self) -> bool:
        if self.subject.house is not None and self.subject.house.ownership_status == OwnershipStatusEnum.mortgaged:
            return True

        return False

    def subject_check_income_min(self, min_income_value: int) -> bool:
        if self.subject.income == 0:
            return False
        return self.subject.income >= min_income_value

    def subject_under_min_age(self, min_age: int) -> bool:
        return self.subject.age < min_age

    def subject_over_max_age(self, max_age: int) -> bool:
        return self.subject.age >= max_age

    def subject_age_range(self, min_age: int, max_age: int) -> bool:
        return min_age < self.subject.age < max_age

    def subject_risk_answers(self) -> int:
        return sum(self.subject.risk_questions)

    def subject_is_married(self) -> bool:
        return self.subject.marital_status == MaritalStatusEnum.married

    def subject_vehicle_age(self) -> bool:
        if self.subject.vehicle is None or self.subject.vehicle.year is None:
            return False

        current_year = datetime.date.today().year
        return (current_year - self.subject.vehicle.year) <= 5

    def subject_has_dependents(self) -> bool:
        return self.subject.dependents > 0

    @staticmethod
    def get_risk_score(risk) -> RiskScoreEnum:
        if risk is RiskScoreEnum.ineligible:
            return RiskScoreEnum.ineligible

        if risk < 1:
            return RiskScoreEnum.economic
        elif risk == 1 or risk == 2:
            return RiskScoreEnum.regular

        return RiskScoreEnum.responsible

    def parse_risk_profile(self, risk_profile: dict) -> dict:
        return {
            "auto": self.get_risk_score(risk_profile["auto"]),
            "disability": self.get_risk_score(risk_profile["disability"]),
            "home": self.get_risk_score(risk_profile["home"]),
            "life": self.get_risk_score(risk_profile["life"]),
        }

    def calculate_subject_score(self) -> RiskProfile:

        initial_risk_value = self.subject_risk_answers()
        risk_profile = {
            "auto": initial_risk_value,
            "home": initial_risk_value,
            "life": initial_risk_value,
            "disability": initial_risk_value,
        }

        if self.subject_check_income_min(MIN_INCOME) is not True:
            risk_profile["auto"] = RiskScoreEnum.ineligible
            risk_profile["home"] = RiskScoreEnum.ineligible
            risk_profile["life"] = RiskScoreEnum.ineligible
            risk_profile["disability"] = RiskScoreEnum.ineligible
            return risk_profile

        if self.subject_check_income_min(MIN_INCOME_THRESHOLD) is not True:
            risk_profile["auto"] -= 1
            risk_profile["home"] -= 1
            risk_profile["life"] -= 1
            risk_profile["disability"] -= 1

        if self.subject_has_mortgaged_house():
            risk_profile["home"] += 1
            risk_profile["disability"] -= 1

        if self.subject_has_dependents():

            risk_profile["home"] += 1
            risk_profile["disability"] += 1

        if self.subject_is_married():
            risk_profile["life"] += 1
            risk_profile["disability"] -= 1

        if self.subject_vehicle_age():
            risk_profile["auto"] = risk_profile["auto"] + 1

        if self.subject_age_range(MIN_AGE_LIMIT, MAX_AGE_LIMIT):
            risk_profile["auto"] -= 1
            risk_profile["home"] -= 1
            risk_profile["life"] -= 1
            risk_profile["disability"] -= 1

        if self.subject_under_min_age(MIN_AGE_LIMIT):

            risk_profile["auto"] -= 2
            risk_profile["home"] -= 2
            risk_profile["life"] -= 2
            risk_profile["disability"] -= 2

        if self.subject_over_max_age(MAX_AGE_LIMIT) is True:
            risk_profile["disability"] = RiskScoreEnum.ineligible
            risk_profile["life"] = RiskScoreEnum.ineligible

        return self.parse_risk_profile(risk_profile)
