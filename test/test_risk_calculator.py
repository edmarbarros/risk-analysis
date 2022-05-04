import unittest

from src.risk_analysis.schemas.personal_information_schema import PersonalInformationSchema
from src.risk_analysis.risk_calculator import RiskCalculator
from src.risk_analysis.risk_analysis_constants import MAX_AGE_LIMIT, MIN_AGE_LIMIT, MIN_INCOME, MIN_INCOME_THRESHOLD
from src.risk_analysis.schemas.risk_score import RiskScoreEnum, RiskProfile


class TestRiskCalculator(unittest.TestCase):

    def test_subject_has_owned_house(self):
        subject = PersonalInformationSchema(
                age=35,
                dependents=2,
                house={"ownership_status": "owned"},
                income=0,
                marital_status="married",
                risk_questions=[0, 1, 0],
                vehicle={"year": 2018},
            )

        result = RiskCalculator(subject).subject_has_mortgaged_house()
        self.assertFalse(result)

    def test_subject_has_mortgaged_house(self):
        subject = PersonalInformationSchema(
                age=35,
                dependents=2,
                house={"ownership_status": "mortgaged"},
                income=0,
                marital_status="married",
                risk_questions=[0, 1, 0],
                vehicle={"year": 2018},
            )

        result = RiskCalculator(subject).subject_has_mortgaged_house()
        self.assertTrue(result)

    def test_subject_has_no_house(self):
        subject = PersonalInformationSchema(
                age=35,
                dependents=2,
                income=0,
                marital_status="married",
                risk_questions=[0, 1, 0],
                vehicle={"year": 2018},
            )

        result = RiskCalculator(subject).subject_has_mortgaged_house()
        self.assertFalse(result)

    def test_subject_has_no_income(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=0,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_check_income_min(MIN_INCOME)
        self.assertFalse(result)

    def test_subject_has_income(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=100000,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_check_income_min(MIN_INCOME)
        self.assertTrue(result)

    def test_subject_has_min_threshold_income(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_check_income_min(MIN_INCOME_THRESHOLD)
        self.assertTrue(result)

    def test_subject_under_min_age(self):
        subject = PersonalInformationSchema(
            age=29,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_under_min_age(MIN_AGE_LIMIT)
        self.assertTrue(result)

    def test_subject_over_max_age(self):
        subject = PersonalInformationSchema(
            age=65,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_over_max_age(MAX_AGE_LIMIT)
        self.assertTrue(result)

    def test_subject_age_range(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 1, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_age_range(MIN_AGE_LIMIT, MAX_AGE_LIMIT)
        self.assertTrue(result)

    def test_subject_risk_answers_all_true(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[1, 1, 1],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_risk_answers()
        self.assertEqual(result, 3)

    def test_subject_risk_answers_all_false(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 0, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_risk_answers()
        self.assertEqual(result, 0)

    def test_subject_is_married(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="married",
            risk_questions=[0, 0, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_is_married()
        self.assertTrue(result)

    def test_subject_is_not_married(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="single",
            risk_questions=[0, 0, 0],
            vehicle={"year": 2018},
        )

        result = RiskCalculator(subject).subject_is_married()
        self.assertFalse(result)

    def test_subject_vehicle_age_under_five_years(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="single",
            risk_questions=[0, 0, 0],
            vehicle={"year": 2020},
        )

        result = RiskCalculator(subject).subject_vehicle_age()
        self.assertTrue(result)

    def test_subject_vehicle_age_over_five_years(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="single",
            risk_questions=[0, 0, 0],
            vehicle={"year": 2010},
        )

        result = RiskCalculator(subject).subject_vehicle_age()
        self.assertFalse(result)

    def test_subject_no_vehicle(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=200000,
            marital_status="single",
            risk_questions=[0, 0, 0],
        )

        result = RiskCalculator(subject).subject_vehicle_age()
        self.assertFalse(result)

    def test_calculate_subject_score_no_income(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=0,
            marital_status="single",
            risk_questions=[0, 0, 0],
        )

        result = RiskCalculator(subject).calculate_subject_score()
        self.assertEqual(
            result,
            RiskProfile(
                auto=RiskScoreEnum.ineligible,
                home=RiskScoreEnum.ineligible,
                life=RiskScoreEnum.ineligible,
                disability=RiskScoreEnum.ineligible,
            )
        )

    def test_calculate_subject_score_min_income(self):
        subject = PersonalInformationSchema(
            age=35,
            dependents=2,
            income=100000,
            marital_status="single",
            risk_questions=[0, 0, 0],
        )

        result = RiskCalculator(subject).calculate_subject_score()
        self.assertEqual(
            result,
            RiskProfile(
                auto=RiskScoreEnum.economic,
                home=RiskScoreEnum.economic,
                life=RiskScoreEnum.economic,
                disability=RiskScoreEnum.economic,
            )
        )


if __name__ == '__main__':
    unittest.main()
