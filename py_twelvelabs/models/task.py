
from datetime import datetime
from typing import Text, Dict, Optional
from pydantic import BaseModel, validator


class Task(BaseModel):
    """
    Task model.
    """

    _id: Text
    index_id: Text
    video_id: Optional[Text] = None
    status: Text
    metadata: Dict
    created_at: datetime
    updated_at: datetime
    type: Optional[Text] = None
    estimated_time: Optional[datetime] = None

    @validator("created_at", "updated_at", "estimated_time", pre=True, allow_reuse=True)
    def parse_date(cls, value):
        formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"time data '{value}' does not match any of the formats {formats}")
    

class TaskStatus(BaseModel):
    """
    Task status model.
    """

    index_id: Text
    ready: int
    validating: int
    pending: int
    failed: int
    total_result: int