from pydantic import BaseModel, Field

from enum import Enum


class RiskScoreEnum(str, Enum):
    economic = "economic"
    regular = "regular"
    responsible = "responsible"
    ineligible = "ineligible"


class RiskProfile(BaseModel):
    auto: RiskScoreEnum = Field(title="The subject eligibility to vehicle insurance")
    disability: RiskScoreEnum = Field(title="The subject eligibility to disability insurance")
    home: RiskScoreEnum = Field(title="The subject eligibility to home insurance")
    life: RiskScoreEnum = Field(title="The subject eligibility to life insurance")
