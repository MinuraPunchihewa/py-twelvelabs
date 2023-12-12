
from datetime import datetime
from pydantic import BaseModel, validator
from typing import Text, Dict


class Task(BaseModel):
    """
    Task model.
    """

    _id: Text
    index_id: Text
    status: Text
    metadata: Dict
    created_at: datetime
    updated_at: datetime
    estimated_time: datetime

    @validator("created_at", "updated_at", "estimated_time", pre=True, allow_reuse=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")