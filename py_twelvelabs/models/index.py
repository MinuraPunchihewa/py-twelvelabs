from datetime import datetime
from typing import Text, List, Optional
from pydantic import BaseModel, validator


class Index(BaseModel):
    """
    Index model.
    """

    _id: Text
    index_name: Text
    index_options: List[Text]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    engine_id: Text
    video_count: int
    total_duration: float
    addons: Optional[List[Text]]
    deleted: Optional[bool] = False

    @validator("created_at", "updated_at", "expires_at", pre=True, allow_reuse=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")