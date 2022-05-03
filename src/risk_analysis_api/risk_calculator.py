import datetime

from src.risk_analysis_api.schemas.personal_information_schema import PersonalInformationSchema, OwnershipStatusEnum, \
    MaritalStatusEnum, VehicleSchema, HouseSchema

from .schemas.risk_score import RiskProfile, RiskScoreEnum
from .risk_analysis_constants import MAX_AGE_LIMIT, MIN_AGE_LIMIT, MIN_INCOME, MIN_INCOME_THRESHOLD


class RiskCalculator:

    def __init__(self) -> None:
        pass

    def subject_has_mortgaged_house(self, house: HouseSchema) -> bool:
        if house is not None and house.ownership_status == OwnershipStatusEnum.mortgaged:
            return True

        return False

    def subject_check_income(self, income: int, income_value: int) -> bool:
        return income > income_value

    def subject_age_min(self, age: int) -> bool:
        return age < MIN_AGE_LIMIT

    def subject_age_range(self, age: int) -> bool:
        return MIN_AGE_LIMIT < age < MAX_AGE_LIMIT

    def subject_age_max(self, age: int) -> bool:
        return age >= MAX_AGE_LIMIT

    def subject_risk_answers(self, risk_questions: List) -> int:
        return sum(risk_questions)

    def subject_is_married(self, marital_status: MaritalStatusEnum) -> bool:
        return marital_status == MaritalStatusEnum.married

    @staticmethod
    def subject_vehicle_age(vehicle: VehicleSchema) -> bool:
        print(vehicle)
        if vehicle is None or vehicle.year is None:
            return False

        current_year = datetime.date.today().year
        return (current_year - vehicle.year) <= 5

    @staticmethod
    def subject_has_dependents(dependents: int) -> bool:
        return dependents > 0

    def get_risk_score(self, risk) -> RiskScoreEnum:
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

    def calculate_subject_score(self, subject: PersonalInformationSchema) -> RiskProfile:

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
