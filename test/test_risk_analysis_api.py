from src.risk_analysis_api import __version__

from fastapi.testclient import TestClient

from src.main import app
from src.risk_analysis_api.schemas.risk_score import RiskScoreEnum

client = TestClient(app)


def test_version():
    assert __version__ == '0.1.0'


def test_run_risk_analysis_empty_body():
    body_data = {}
    response = client.post("/risk-analysis", data=body_data)
    assert response.status_code == 422


def test_run_risk_analysis_ineligible_income():
    body_data = '{ \
            "age": 35, \
            "dependents": 2, \
            "house": {"ownership_status": "owned"}, \
            "income": 0, \
            "marital_status": "married", \
            "risk_questions": [0, 1, 0], \
            "vehicle": {"year": 2018} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.ineligible,
        'disability': RiskScoreEnum.ineligible,
        'home': RiskScoreEnum.ineligible,
        'life': RiskScoreEnum.ineligible
    }


def test_run_risk_analysis_under_min_age_risk():
    body_data = '{ \
            "age": 25, \
            "dependents": 0, \
            "house": {"ownership_status": "owned"}, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [0, 0, 0], \
            "vehicle": {"year": 2020} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.economic,
        'disability': RiskScoreEnum.economic,
        'home': RiskScoreEnum.economic,
        'life': RiskScoreEnum.economic
    }


def test_run_risk_analysis_above_max_age_risk():
    body_data = '{ \
            "age": 65, \
            "dependents": 0, \
            "house": {"ownership_status": "owned"}, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [0, 0, 0], \
            "vehicle": {"year": 2020} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.economic,
        'disability': RiskScoreEnum.ineligible,
        'home': RiskScoreEnum.economic,
        'life': RiskScoreEnum.ineligible
    }


def test_run_risk_analysis_age_in_range():
    body_data = '{ \
            "age": 30, \
            "dependents": 0, \
            "house": {"ownership_status": "owned"}, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [0, 0, 0], \
            "vehicle": {"year": 2020} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.economic,
        'disability': RiskScoreEnum.economic,
        'home': RiskScoreEnum.economic,
        'life': RiskScoreEnum.economic
    }


def test_run_risk_analysis_age_in_range_with_dependents():
    body_data = '{ \
            "age": 35, \
            "dependents": 3, \
            "house": {"ownership_status": "owned"}, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [0, 0, 0], \
            "vehicle": {"year": 2020} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.economic,
        'disability': RiskScoreEnum.economic,
        'home': RiskScoreEnum.economic,
        'life': RiskScoreEnum.economic
    }


def test_run_risk_analysis_age_in_range_with_dependents_and_mortgaged_and_risks():
    body_data = '{ \
            "age": 35, \
            "dependents": 3, \
            "house": {"ownership_status": "mortgaged"}, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [1, 1, 1], \
            "vehicle": {"year": 2020} \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.regular,
        'disability': RiskScoreEnum.regular,
        'home': RiskScoreEnum.responsible,
        'life': RiskScoreEnum.regular
    }


def test_run_risk_analysis_age_in_range_no_dependents_no_house_no_vehicle():
    body_data = '{ \
            "age": 35, \
            "dependents": 0, \
            "income": 100000, \
            "marital_status": "single", \
            "risk_questions": [1, 1, 1] \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.regular,
        'disability': RiskScoreEnum.regular,
        'home': RiskScoreEnum.regular,
        'life': RiskScoreEnum.regular
    }


def test_run_risk_analysis_age_in_range_no_dependents_no_house_no_vehicle_and_high_income():
    body_data = '{ \
            "age": 35, \
            "dependents": 0, \
            "income": 250000, \
            "marital_status": "married", \
            "risk_questions": [1, 1, 0] \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.regular,
        'disability': RiskScoreEnum.economic,
        'home': RiskScoreEnum.regular,
        'life': RiskScoreEnum.regular
    }


def test_run_risk_analysis_age_in_range_and_married_with_dependents_no_house_no_vehicle_and_high_income():
    body_data = '{ \
            "age": 35, \
            "dependents": 2, \
            "income": 250000, \
            "marital_status": "married", \
            "risk_questions": [1, 1, 1] \
        }'
    response = client.post("/risk-analysis", data=body_data)
    print('response.json()')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'auto': RiskScoreEnum.regular,
        'disability': RiskScoreEnum.regular,
        'home': RiskScoreEnum.responsible,
        'life': RiskScoreEnum.responsible
    }