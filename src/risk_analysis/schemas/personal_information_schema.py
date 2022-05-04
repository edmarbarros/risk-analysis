import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class OwnershipStatusEnum(str, Enum):
    owned = "owned"
    mortgaged = "mortgaged"


class MaritalStatusEnum(str, Enum):
    single = "single"
    married = "married"


class VehicleSchema(BaseModel):
    year: int = Field(title="The vehicle build year", ge=1886, lt=datetime.date.today().year)


class HouseSchema(BaseModel):
    ownership_status: OwnershipStatusEnum = Field(title="The house ownership status")


class PersonalInformationSchema(BaseModel):
    age: int = Field(title="The age of the person to run the risk analysis", ge=0)
    dependents: int = Field(title="The number of dependents of person to run the risk analysis", ge=0)
    house: Optional[HouseSchema] = Field(title="The house ownership details")
    income: int = Field(title="The income of person to run the risk analysis", ge=0)
    marital_status: MaritalStatusEnum = Field(title="The marital status of person to run the risk analysis")
    risk_questions: List[bool] = Field(..., min_items=3, max_items=3)
    vehicle: Optional[VehicleSchema]
