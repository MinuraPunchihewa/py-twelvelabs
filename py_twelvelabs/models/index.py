from pydantic import BaseModel, Extra
from typing import Text, List, Dict, Optional, Any


class Index(BaseModel):
    """
    Index model.
    """

    _id: Text
    index_name: Text
    index_options: List[Text]
    created_at: Text
    updated_at: Text
    engine_id: Text
    video_count: int
    total_duration: float
    addons: List[Text]
