# Origin Backend Take-Home Assignment
Origin offers its users an insurance package personalized to their specific needs without requiring the user to understand anything about insurance. This allows Origin to act as their *de facto* insurance advisor.

Origin determines the user’s insurance needs by asking personal & risk-related questions and gathering information about the user’s vehicle and house. Using this data, Origin determines their risk profile for **each** line of insurance and then suggests an insurance plan (`"economic"`, `"regular"`, `"responsible"`) corresponding to her risk profile.

For this assignment, you will create a simple version of that application by coding a simple API endpoint that receives a JSON payload with the user information and returns her risk profile (JSON again) – you don’t have to worry about the frontend of the application.

## The input
First, the would-be frontend of this application asks the user for her **personal information**. Then, it lets her add her **house** and **vehicle**. Finally, it asks her to answer 3 binary **risk questions**. The result produces a JSON payload, posted to the application’s API endpoint, like this example:

```JSON
{
  "age": 35,
  "dependents": 2,
  "house": {"ownership_status": "owned"},
  "income": 0,
  "marital_status": "married",
  "risk_questions": [0, 1, 0],
  "vehicle": {"year": 2018}
}
```

### User attributes
All user attributes are required:

- Age (an integer equal or greater than 0).
- The number of dependents (an integer equal or greater than 0).
- Income (an integer equal or greater than 0).
- Marital status (`"single"` or `"married"`).
- Risk answers (an array with 3 booleans).

### House
Users can have 0 or 1 house. When they do, it has just one attribute: `ownership_status`, which can be `"owned"` or `"mortgaged"`.

### Vehicle
Users can have 0 or 1 vehicle. When they do, it has just one attribute: a positive integer corresponding to the `year` it was manufactured.

## The risk algorithm
The application receives the JSON payload through the API endpoint and transforms it into a *risk profile* by calculating a *risk score* for each line of insurance (life, disability, home & auto) based on the information provided by the user.

First, it calculates the *base score* by summing the answers from the risk questions, resulting in a number ranging from 0 to 3. Then, it applies the following rules to determine a *risk score* for each line of insurance.

1. If the user doesn’t have income, vehicles or houses, she is ineligible for disability, auto, and home insurance, respectively.
2. If the user is over 60 years old, she is ineligible for disability and life insurance.
3. If the user is under 30 years old, deduct 2 risk points from all lines of insurance. If she is between 30 and 40 years old, deduct 1.
4. If her income is above $200k, deduct 1 risk point from all lines of insurance. 
5. If the user's house is mortgaged, add 1 risk point to her home score and add 1 risk point to her disability score. 
6. If the user has dependents, add 1 risk point to both the disability and life scores. 
7. If the user is married, add 1 risk point to the life score and remove 1 risk point from disability. 
8. If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.

This algorithm results in a final score for each line of insurance, which should be processed using the following ranges:

- **0 and below** maps to **“economic”**.
- **1 and 2** maps to **“regular”**.
- **3 and above** maps to **“responsible”**.


## The output
Considering the data provided above, the application should return the following JSON payload:

```JSON
{
    "auto": "regular",
    "disability": "ineligible",
    "home": "economic",
    "life": "regular"
}
```

## Criteria
You may use any language and framework provided that you build a solid system with an emphasis on code quality, simplicity, readability, maintainability, and reliability, particularly regarding architecture and testing. We'd prefer it if you used Python, but it's just that – a preference.

Be aware that Origin will mainly take into consideration the following evaluation criteria:
* How clean and organized your code is;
* If you implemented the business rules correctly;
* How good your automated tests are (qualitative over quantitative).

Other important notes:
* Develop a extensible score calculation engine
* Add to the README file: (1) instructions to run the code; (2) what were the main technical decisions you made; (3) relevant comments about your project 
* You must use English in your code and also in your docs

This assignment should be doable in less than one day. We expect you to learn fast, **communicate with us**, and make decisions regarding its implementation & scope to achieve the expected results on time.

It is not necessary to build the screens a user would interact with, however, as the API is intended to power a user-facing application, we expect the implementation to be as close as possible to what would be necessary in real-life. Consider another developer would get your project/repository to evolve and implement new features from exactly where you stopped. 


# Development Notes

In order to keep the code DRY and define the responsibilities of each class, I divide the code into the following main parts:
 - main.py - Start the service and load the individual modules:
 - src/risk_analysis - Module to handle the Risk Analysis API

Each module should represent a base endpoint, in this case, this module handles the `risk-analysis`.

- risk_analysis_constants - To keep the code organized and reduce the use of magic strings/numbers
- risk_analysis_controller - Describe the API endpoints that handle the incoming HTTP requests
- risk_analysis_service - Handle the Business logic and data manipulation
- risk_calculator - Score Calculator 

The Score Calculator is a Class that will handle all the Risk Calculation Rules.


### API Documentation
On of the advantages of FastAPI is the API documentation that is generated based on the [Pydantic](https://pydantic-docs.helpmanual.io/) Models and the Controller definition.


OpenAPI - http://127.0.0.1:8000/docs

Redoc - http://127.0.0.1:8000/redoc


### API Error Responses

If a mandatory field is not present, the application consuming the endpoints will be able to map it precisely to the end user using the following error response:  

#### Missing mandatory Field
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "risk_questions"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
#### Invalid Field Type
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "dependents"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
} 
```
#### Invalid Value
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "age"
      ],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge",
      "ctx": {
        "limit_value": 0
      }
    }
  ]
}
```

### Technology

The solution was developed using Python 3.9, [FastAPI Framework](https://fastapi.tiangolo.com/) and [Poetry](https://python-poetry.org/) as a package dependency management following the [PEP 8](https://peps.python.org/pep-0008/) code convention.


### Requirements 

- [Python 3.9](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Usage

Install dependencies:
```
$ poetry install 
```

Start the server:
```
$ poetry run start
```

### Tests
Run Tests with coverage report:
```
$ poetry run pytest -vv --cov=.
```

```
---------- coverage: platform darwin, python 3.9.10-final-0 ----------
Name                                                           Stmts   Miss  Cover
----------------------------------------------------------------------------------
src/main.py                                                       20      7    65%
src/risk_analysis_api/__init__.py                                  1      0   100%
src/risk_analysis_api/risk_analysis_constants.py                   4      0   100%
src/risk_analysis_api/risk_analysis_controller.py                  8      0   100%
src/risk_analysis_api/risk_analysys_service.py                     8      0   100%
src/risk_analysis_api/risk_calculator.py                          84      0   100%
src/risk_analysis_api/schemas/__init__.py                          0      0   100%
src/risk_analysis_api/schemas/personal_information_schema.py      22      0   100%
src/risk_analysis_api/schemas/risk_score.py                       12      0   100%
test/__init__.py                                                   0      0   100%
test/test_main.py                                                  7      0   100%
test/test_risk_analysis_api.py                                    72      0   100%
test/test_risk_calculator.py                                      80      1    99%
----------------------------------------------------------------------------------
TOTAL                                                            318      8    97%

```

### Project Structure

```
.
|____pytest.ini
|____pyproject.toml                         # Project Configuration
|____README.md
|____poetry.lock
|____test                                   # Global Tests directory 
| |____test_risk_analysis_api.py
| |____test_risk_calculator.py
| |____test_main.py
|____src                                    # Modules Root
| |____risk_analysis_api                    # Risk Analysis Module
| | |____schemas                            # Data Models
| | | |____personal_information_schema.py   
| | | |____risk_score.py
| | |____risk_calculator.py                 # Risk Calculator
| | |____risk_analysis_constants.py         # Module Constant
| | |____risk_analysis_controller.py        # API Controller
| | |____risk_analysys_service.py           # API Service
| |____main.py                              # Main server

```

### Improvements to make it Production ready


- [ ] Expand uvicorn log configuration and add logs to trace the request lifecycle 
- [ ] Health Monitor
- [ ] API Authentication and Authorization
- [ ] Rate Limit
- [ ] Containerization
- [ ] Configure a linter to enforce code style
- [ ] Configure Semantic Release with commit pre-fixes
- [ ] Use pre-commit/push hooks to run validations(tests, lint..) 
