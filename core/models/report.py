from typing import TypeVar, Generic

from pydantic import BaseModel, validator

T = TypeVar("T")


class MonthlyReport(BaseModel, Generic[T]):
    month: int
    data: T

    @validator("month")
    def validate_month(cls, value: int):
        if value < 1 or value > 12:
            raise ValueError("Invalid month attribute. Accepted value: from 1 to 12")
        return value
